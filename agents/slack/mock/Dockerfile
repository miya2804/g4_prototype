FROM golang:1.14.4-alpine3.11

RUN apk --update add alpine-sdk
RUN go get gopkg.in/ini.v1

WORKDIR /go/src/github.com/agent

CMD ["go", "run", "app.go"]