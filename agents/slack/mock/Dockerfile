FROM golang:1.14.4-alpine3.11

RUN apk --update add alpine-sdk

WORKDIR /go/src/github.com/agent

CMD ["go", "run", "app.go"]