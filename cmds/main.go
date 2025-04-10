package main

import (
	"os"
	"pass-coding-interview/internal/outbound/argocd"
	"pass-coding-interview/internal/outbound/datadog"
)

func main() {
	applicationFlag := "test"
	// check if the file
	scheduleId, err := datadog.CreateSchedule(applicationFlag)
	if err != nil {
		os.Exit(1)
	}
	// check if there is an application currently sync
	err = argocd.SyncArgoCDApp(applicationFlag)
	if err != nil {
		os.Exit(2)
	}
	err = datadog.CancelSchedule(scheduleId)
	if err != nil {
		os.Exit(3)
	}
}
