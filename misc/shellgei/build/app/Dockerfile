FROM golang:1.18-alpine

ENV NAME SHELLGEI_APP

WORKDIR /go/src/app

RUN apk add --no-cache bash
RUN rm /usr/bin/wget

COPY . .
RUN go mod download
RUN CGO_ENABLED=0 go build -o /go/src/app/shellgei .
RUN chmod a+rw /go/src/app/scripts
RUN chmod a-wx /go/src/app/flag.txt

RUN addgroup -S shellgei && adduser -S shellgei -G shellgei
USER shellgei

CMD ["/go/src/app/shellgei"]
