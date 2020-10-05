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
	"gopkg.in/ini.v1"
)

const (
	INTERVAL = time.Duration(10 * time.Second)
)

type Config struct {
	Url string
	Data_content_type string
	Room_id string
	Password string
	Api_url string
	Request_url string
}

type Data struct {
	Text string `json:"text"`
}

type Rasps map[int]Rasp

type Rasp struct {
	State States `json:"state"`
}

type States struct {
	 Opened bool `json:"opened"`
}

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	wg := &sync.WaitGroup{}

	var Cnf Config
	c, err := ini.Load("config.ini")
	if err != nil {
		panic(err)
	}
	Cnf = Config {
		Url : c.Section("webhook").Key("url").String(),
		Data_content_type : c.Section("data").Key("data_content_type").String(),
		Room_id : c.Section("room").Key("room_id").String(),
		Password : c.Section("room").Key("password").String(),
		Api_url : c.Section("api").Key("url").String(),
	}
	Cnf.Request_url = Cnf.Api_url + Cnf.Room_id + "?password=" + Cnf.Password

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
				rst, err := http.Get(Cnf.Request_url)
				if err != nil {
					log.Println(err)
					continue
				}

				defer rst.Body.Close()
 
				body, err := ioutil.ReadAll(rst.Body)
				if err != nil {
					log.Println(err)
					continue
				}

				var states Rasps
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
					log.Println(open)
					cnt_open += isOpened(open.State.Opened)
				}
				
				if (cnt_open < 2) {
					data, err := json.Marshal(&Data{
						Text: "Please ventilate!",
					})
					if err != nil {
						log.Println(err)
						continue
					}

					resp, err := http.Post(Cnf.Url, Cnf.Data_content_type, bytes.NewBuffer(data))
					if err != nil {
						log.Println(err)
						continue
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