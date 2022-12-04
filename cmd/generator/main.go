package main

import (
	"bytes"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"text/template"

	_ "embed"

	"github.com/manifoldco/promptui"
)

var (
	//go:embed templates/challenge.yml.tmpl
	challengeTemplate string

	genres []string = []string{"misc", "web", "rev", "pwn", "osint"}

	challengeFormat = "^[a-z0-9_!?]+$"
	challengeRegExp = regexp.MustCompile(challengeFormat)

	flagFormat = "^taskctf{[a-zA-Z0-9_!?]+}$"
	flagRegExp = regexp.MustCompile(flagFormat)
)

func main() {
	// get genre
	promptForSelect := promptui.Select{
		Label: "genre",
		Items: genres,
	}
	_, genre, err := promptForSelect.Run()
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed promptForSelect.Run(): %s", err.Error())
		os.Exit(1)
	}

	// get challenge name
	prompt := promptui.Prompt{
		Label: "challenge name",
		Validate: func(input string) error {
			if !challengeRegExp.MatchString(input) {
				return fmt.Errorf("challengeName should meet %s", challengeFormat)
			}

			return nil
		},
	}
	challengeName, err := prompt.Run()
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed prompt.Run() for challengeName: %s", err.Error())
		os.Exit(1)
	}
	// forced to lower case
	challengeName = strings.ToLower(challengeName)

	// get author name
	prompt.Label = "author name"
	author, err := prompt.Run()
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed prompt.Run() for author: %s", err.Error())
		os.Exit(1)
	}

	// get flag
	prompt = promptui.Prompt{
		Label: "flag",
		Validate: func(input string) error {
			if !flagRegExp.MatchString(input) {
				return fmt.Errorf("flag should meet %s", flagFormat)
			}
			return nil
		},
	}
	flag, err := prompt.Run()
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed prompt.Run(): %s", err.Error())
		os.Exit(1)
	}

	// ready a directory structure
	// - make directory(./genre/challengeName)
	//   - directory: build, files, solver
	//   - file: README.md, flag.txt, challenge.yml
	err = os.MkdirAll(filepath.Join(genre, challengeName), os.ModePerm)
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed os.MkdirAll(genre/challengeName): %s", err.Error())
		os.Exit(1)
	}

	dirs := []string{"build", "files", "solver"}
	for _, dirName := range dirs {
		err = os.MkdirAll(filepath.Join(genre, challengeName, dirName), os.ModePerm)
		if err != nil {
			fmt.Fprintf(os.Stderr, "failed os.MkdirAll(genre/challengeName/%s): %s", dirName, err.Error())
			os.Exit(1)
		}
	}

	// write default description for each file
	files := []string{"README.md", "flag.txt"}
	for _, fileName := range files {
		fp, err := os.Create(filepath.Join(genre, challengeName, fileName))
		if err != nil {
			fmt.Fprintf(os.Stderr, "failed os.Create(genre/challengeName/%s): %s", fileName, err.Error())
			os.Exit(1)
		}
		defer fp.Close()

		// write template message
		if fileName == "README.md" {
			fmt.Fprintf(fp, "## %s\n\n### 作問者\n%s\n\n### 問題文\nTODO: 書く\n\n### 難易度\nTODO: 書く\n\n## メモ\n\n", challengeName, author)
		}
		if fileName == "flag.txt" {
			fmt.Fprintln(fp, flag)
		}
	}

	// ready challenge.yml
	tpl, err := template.New("challenge").Parse(challengeTemplate)
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed template.New: %s", err.Error())
		os.Exit(1)
	}
	writer := &bytes.Buffer{}
	err = tpl.Execute(writer, struct {
		ChallengeName string
		Author        string
		Genre         string
		Flag          string
	}{
		ChallengeName: challengeName,
		Author:        author,
		Genre:         genre,
		Flag:          flag,
	})
	fp, err := os.Create(filepath.Join(genre, challengeName, "challenge.yml"))
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed os.Create(genre/challengeName/challenge.yml): %s", err.Error())
		os.Exit(1)
	}
	defer fp.Close()
	fmt.Fprint(fp, writer.String())
}
