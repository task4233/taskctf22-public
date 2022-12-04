package main

import (
	"fmt"
	"math/rand"
	"net/http"
	"time"
)

const ADDR = ":8888"

func main() {
	rand.Seed(time.Now().UnixNano())
	http.HandleFunc("/bD7bB7pc57d2", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "%d", rand.Intn(0x11000))
	})
	http.ListenAndServe(ADDR, nil)
}
