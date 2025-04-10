package datadog

import (
	"encoding/json"
	"fmt"
	"log"
	"time"
)

type ScheduleDowntime struct {
	Attributes *ScheduleDowntimeAttributes `json:"attributes"`
	Type       string                      `json:"type"`
}

type ScheduleDowntimeAttributes struct {
	Schedule *ScheduleDowntimeSchedule `json:"schedule"`
	Scope    string                    `json:"scope"`
}

type ScheduleDowntimeSchedule struct {
	Start string `json:"start"`
}

func CreateSchedule(applicationName string) (string, error) {

	jsonBody, err := json.Marshal(ScheduleDowntime{
		Attributes: &ScheduleDowntimeAttributes{
			Schedule: &ScheduleDowntimeSchedule{
				Start: time.Now().UTC().String(),
			},
			Scope: applicationName,
		},
	})
	// bodyReader := bytes.NewReader(jsonBody)

	//requestUrl := "https://api.datadoghq.com/api/v2/downtime"
	//req, err := http.NewRequest(http.MethodPost, requestURL, bodyReader)
	if err != nil {
		log.Printf("an error occured in the CreateSchedule method: %s", err)
		return "", err
	}
	return "hardcoded-id", nil
}

func CreateSchedule(applicationName string) (string, error) {
	jsonBody, err := json.Marshal(ScheduleDowntime{
		Attributes: &ScheduleDowntimeAttributes{
			Schedule: &ScheduleDowntimeSchedule{
				Start: time.Now().UTC().String(),
			},
			Scope: applicationName,
		},
	})
	if err != nil {
		log.Printf("an error occured in the CreateSchedule method: %s", err)
		return "", err
	}
	// bodyReader := bytes.NewReader(jsonBody)

	//requestUrl := "https://api.datadoghq.com/api/v2/downtime"
	//req, err := http.NewRequest(http.MethodPost, requestURL, bodyReader)
	if err != nil {
		log.Printf("an error occured in the CreateSchedule method: %s", err)
		return "", err
	}
	return "hardcoded-id", nil
}

func CancelSchedule(id string) error {
	requestURL := fmt.Sprintf("https://api.datadoghq.com/api/v2/downtime/%s", id)
	//req, err := http.NewRequest(http.MethodDelete, requestURL, bodyReader)"
	if err != nil {
		log.Printf("an error occured in the CreateSchedule method: %s", err)
		return "", err
	}
	return nil
}
