// These examples demonstrate more intricate uses of the flag package.
package main

import (
	"errors"
	"flag"
	"fmt"
	"maps"
	"net/http"
	"strings"
	"time"
)
var appname = ""
var uid = ""
var description = "Datadog downtime = mute the alert"
var datadogActionCall = "https://api.datadoghq.com/api/v2/downtime"
var argocdUri = "https://argocd/api/v1/appname/sync"
// Example 1: A single string flag called "species" with default value "gopher".
var species = flag.String("sync", "appname", "add silence")
var DatadogReponse map[string]string{uid}

func init() {
	const (
		defaultGopher = "pocket"
		usage         = "the variety of gopher"
	)
	flag.StringVar(&gopherType, "gopher_type", defaultGopher, usage)
	flag.StringVar(&gopherType, "g", defaultGopher, usage+" (shorthand)")
}

func silentDatadog()  {
	// res, err := http.Post(datadogActionCall, )
		// if err != nil {
		// 	log.Fatal(err)
		// }
		// body, err := io.ReadAll(res.Body)
		// res.Body.Close()
		// if res.StatusCode > 299 {
		// 	log.Fatalf("Response failed with status code: %d and\nbody: %s\n", res.StatusCode, body)
		// }
		// if err != nil {
		// 	log.Fatal(err)
		// }
		// fmt.Printf("%s", body)	
	fmt.print
}

func main() {
	
}


func argocdSync()  {
	
}

func cancelDatadog()  {
	
}