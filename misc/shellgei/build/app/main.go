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

func IndexGet(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, indexHtml)
}

func IndexPost(w http.ResponseWriter, r *http.Request) {
	// read given payload
	payload := r.FormValue("payload")
	if len(payload) == 0 {
		log.Println("empty payload")
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode("empty payload is not allowed")
		return
	}

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
	fmt.Fprint(f, strings.Replace(payload, "\r", "", -1))

	// instant waf
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

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// only got stdout
	os.Chmod(fName, 0555)
	out, err := exec.CommandContext(ctx, "/bin/bash", fName).Output()
	if err != nil {
		log.Println("failed to get output", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(fmt.Sprintf("failed to execute command with %s, please send other payload", payload))
		return
	}
	// DO NOT cheating
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
