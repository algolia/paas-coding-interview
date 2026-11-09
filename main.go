package main

import (
	"fmt"
	"os"
)

// struct argument with it
type Sync struct{
	application_name string
}

// func enable_downtime(scope string) -> (bool, string, err)

// func argocd_sync(application_name string) -> (bool, err)

// func remove_downtime(downtime_id string) -> (bool, err)

// func check_app_status(application_name string) -> (bool, err)
// Import argument
func main() {
	application_name := os.Args[0]
	fmt.Println(application_name)
	scope := "scope{{" + application_name +"}}"
	check_enable, downtime_id, err := enable_downtime(scope)
	if err != nil {
		return err
	}
	if check_enable {
		check_argocd_sync, err := argocd_sync(application_name)

		if err != nil {
			check_remove_downtime, err := remove_downtime(downtime_id)
			if err != nil {
				return err
			}
			if check_remove_downtime {
				fmt.Sprintf("Downtime has been removed", application_name)
			}
			return err
		}
		check_app_status()
		if check_argocd_sync {
			check_remove_downtime, err := remove_downtime(downtime_id)
			if err != nil {
				return err
			}
			if check_remove_downtime {
				fmt.Sprintf("You app %s has been sync well", application_name)
			}
		}
	}

}