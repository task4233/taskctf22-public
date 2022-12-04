package main

import (
	"context"
	_ "embed"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/google/uuid"
)

var (
	whitelist = `!"#$%&'()*+,-./:;<=>?@[\]{}^ _\n`

	//go:embed flag.txt
	flag string

	//go:embed templates/index.html
	indexHtml string
)

// IndexGet serves GET /
func IndexGet(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, indexHtml)
}

// IndexPost serves POST /
func IndexPost(w http.ResponseWriter, r *http.Request) {
	// read the given payload.
	payload := r.FormValue("payload")

	// empty payload is not allowed.
	if len(payload) == 0 {
		log.Println("empty payload")
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode("empty payload is not allowed")
		return
	}

	// ready scripts with the given payload
	fName := fmt.Sprintf("scripts/%s.bash", uuid.NewString())
	f, err := os.Create(fName)
	if err != nil {
		log.Printf("failed to create: %s\n", err.Error())
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode("internal server error occurs, please retry :)")
		return
	}
	defer f.Close()
	os.Chmod(fName, 0777)
	fmt.Fprint(f, strings.Replace(payload, "\r", "", -1)) // remove carriage returns because they prevent script execution.

	// check if the given payload is constructed by characters in the whitelist.
	for _, ch := range payload {
		ok := false
		for _, ww := range whitelist {
			ok = ok || (ch == ww)
		}
		if !ok {
			w.WriteHeader(http.StatusBadRequest)
			json.NewEncoder(w).Encode(fmt.Sprintf("%s is not allowed", string(ch)))
			return
		}
	}

	// update the permission Read & eXecution.
	os.Chmod(fName, 0555)

	// the given script is executed in 3 secs.
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	// execute the script and get ONLY stdout, not including stderr.
	out, err := exec.CommandContext(ctx, "/bin/bash", fName).Output()
	if err != nil {
		log.Println("failed to get output", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(fmt.Sprintf("failed to execute command with %s, please send other payload", payload))
		return
	}

	// check if not exposes other information.
	if string(out) != flag {
		log.Println("invalid output")
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode("this response does not contain the expected flag...")
		return
	}

	json.NewEncoder(w).Encode(string(out))
}

func main() {
	r := chi.NewRouter()
	r.Use(middleware.Logger)
	r.Get("/", IndexGet)
	r.Post("/", IndexPost)
	http.ListenAndServe(":8080", r)
}
