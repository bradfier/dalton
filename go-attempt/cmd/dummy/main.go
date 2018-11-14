package main

import (
	"fmt"
	"git.sr.ht/~bradfier/dalton"
)

func main() {
	token := dalton.AccessToken{TokenValue: "bb043692-afd9-4758-85a2-ccbc6e0b8c7b"}

	client := dalton.NewClient("https://lite.realtime.nationalrail.co.uk/OpenLDBWS/ldb6.asmx")
	client.AddHeader(token)

	service := dalton.NewLDBServiceSoap(*client)

	var crs dalton.CRSType = "man"
	request := dalton.GetBoardRequestParams{
		Crs:     &crs,
		NumRows: 10,
	}

	response, err := service.GetDepartureBoard(&request)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(response)
}
