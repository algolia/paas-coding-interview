package argocd

import (
	"fmt"
	"log"
)

func SyncArgoCDApp(applicationName string) error {
	requestURL := fmt.Sprintf("https://cd.apps.argoproj.io/api/v1/applications/%s/sync", applicationName)
	//req, err := http.NewRequest(http.MethodPost, requestURL, bodyReader)
	if err != nil {
		log.Printf("an error occured in the SyncArgoCDApp method: %s", err)
		return "", err
	}
	return nil
}
