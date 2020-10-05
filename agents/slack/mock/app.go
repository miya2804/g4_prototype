package main

import (
	"os"
	"time"
	"sync"
	"bytes"
	"syscall"
	"context"
	"log"
	"io/ioutil"
	"net/http"
	"os/signal"
	"encoding/json"
)

const (
	URI = ""
	DATA_CONTENT_TYPE = "application/json"
	INTERVAL = time.Duration(10 * time.Second)
	room_id = ""
	password = ""
	request_url = "http://master:8080/api/room/" + room_id + "?password=" + password
)


type Data struct {
	Text string `json:"text"`
}

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	wg := &sync.WaitGroup{}

	go func () {
		wg.Add(1)
		ticker := time.NewTicker(INTERVAL)
		defer ticker.Stop()

	Loop:
		for {
			select {
			case <-ctx.Done():
				break Loop
			case <-ticker.C:
				rst, err := http.Get(request_url)
				if err != nil {
					panic(err)
				}

				defer rst.Body.Close()
 
				body, err := ioutil.ReadAll(rst.Body)
				if err != nil {
					panic(err)
				}

				var states map[int]map[string]map[string]bool
				e := json.Unmarshal([]byte(body), &states)
				if e != nil {
					log.Println(e)
					continue
				} else if len(states) == 0 {
					log.Println(states)
					continue
				}

				var cnt_open int
				for _, open := range states {
					log.Println(open["state"])
					cnt_open += isOpened(open["state"]["opened"])
				}
				
				if (cnt_open < 2) {
					data, err := json.Marshal(&Data{
						Text: "Please ventilate!",
					})
					if err != nil {
						panic(err)
					}

					resp, err := http.Post(URI, DATA_CONTENT_TYPE, bytes.NewBuffer(data))
					if err != nil {
						panic(err)
					}
					resp.Body.Close()
				}
			default:
				break
			}
		}
		wg.Done()
	}()

	sigCh := make(chan os.Signal)
	signal.Notify(sigCh, os.Interrupt, syscall.SIGTERM)

	go func () {
		<-sigCh
		cancel()
	}()

	wg.Wait()
}

func isOpened(state bool) int {
	if (state) {
		return 1
	}

	return 0
}