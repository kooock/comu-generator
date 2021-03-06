package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

type Word struct {
	Word string `json:"word"`
	Desc string `json:"desc"`
}

func getWordHandler(wordType string) func(http.ResponseWriter, *http.Request){
	f := func(writer http.ResponseWriter, request *http.Request) {
		writer.Header().Set("Content-Type", "application/json")
		b, err := ioutil.ReadFile(fmt.Sprintf("./assets/%s.json",wordType))
		var data []Word
		if err != nil {
			json.NewEncoder(writer).Encode(data)
		}
		writer.Write(b)
	}
	return f
}

func main()  {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080" // Default port if not specified
	}

	http.Handle("/",http.FileServer(http.Dir("templates")))
	http.HandleFunc("/cos", getWordHandler("co"))
	http.HandleFunc("/mus", getWordHandler("mu"))
	http.ListenAndServe(":" + port, nil)
}