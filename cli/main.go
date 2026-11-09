package main

import (
	//"bytes"
	"fmt"
	//"io/ioutil"
	//"net/http"
	//"os"
	//"strings"
	//"path/filepath"
	"flag"
	"log/slog"
)

var (
	app = flag.String("application", "", "Application name")
)

//func postRequest(client *http.Client, url string, jsonData []byte) error {
//	//body := &bytes.Buffer{}
//	//writer := multipart.NewWriter(body)
//	//part, err := writer.CreateFormFile("file", "example.txt")
//	//if err != nil {
//	//    return fmt.Errorf("Form file creation failed: %v", err)
//	//}
//	//io.WriteString(part, content)
//	//writer.Close()
//
//	//var jsonData = []byte(`{
//	//	"name": "morpheus",
//	//	"job": "leader"
//	//}`)
//	request, error := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
//	request.Header.Set("Content-Type", "application/json; charset=UTF-8")
//
//	client := &http.Client{}
//	response, error := client.Do(request)
//	if error != nil {
//		return error
//	}
//	defer response.Body.Close()
//	if response.Status != "200" {
//		return fmt.Errorf("Bad response")
//	}
//
//	body, _ := ioutil.ReadAll(response.Body)
//	fmt.Println("response Body:", string(body))
//	return nil
//}

func doRequest() {
	response := 200
	if response != 200 {
		return "", fmt.Errorf("Can't silence app %s", appName)
	}
	//Get the downtime id from json
}

func argocdAuth() {
}

func argocdSync(appName string) error {
	if appName != "" {
		return "", fmt.Errorf("Please provide an application name")
		//Test if the app exists
	}
	//Do the request to argocd and check answer
	response := 200
	if response != 200 {
		return "", fmt.Errorf("Can't silence app %s", appName)
	}
	//Get the downtime id from json
	downtimeId := "01"
	return downtimeId, nil

}

func datadogAuth() {
}

func datadogSilent(appName string) (string, error) {
	if appName != "" {
		return "", fmt.Errorf("Please provide an application name")
		//Test if the app exists
	}
	//Do the request to datadog and check answer
	response := 200
	if response != 200 {
		return "", fmt.Errorf("Can't silence app %s", appName)
	}
	//Get the downtime id from json
	downtimeId := "01"
	return downtimeId, nil
}

func datadogUnSilent(downtimeId string, appName string) error {
	if appName != "" {
		return fmt.Errorf("Please provide an application name")
		//Test if the app exists
	}
	//Test if downtimeId exists
	//Do the request to datadog and check answer
	response := 200
	if response != 200 {
		return fmt.Errorf("Can't unsilence app %s", appName)
	}
}

func main() {
	flag.Parse()
	slog.Info("Using app", *app)
	fmt.Println(*app)
	slog.Info("Silence Datadog")
	downtimeId, err := datadogSilent(*app)
	if err != nil {
		log.Fatal(err)
	}
	slog.Info("ArgoCD sync")
	err := argocdSync(*app)
	if err != nil {
		log.Fatal(err)
	}
	slog.Info("Unsilence Datadog")
	err := datadogUnSilent(downtimeId, *app)
	if err != nil {
		log.Fatal(err)
	}

}
