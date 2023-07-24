FROM node:lts-alpine as builder

ARG RECAPTCHA_SITEKEY
ENV RECAPTCHA_SITEKEY=${RECAPTCHA_SITEKEY}
WORKDIR /usr/client-dist
ADD ./webapp/client /usr/client-dist
RUN npm run build


FROM golang:1.20-alpine

WORKDIR /usr/src/app/webapp
ADD . /usr/src/app
RUN go build -v -o webapp
COPY --from=builder /usr/client-dist/dist ./client/dist
EXPOSE 3000

CMD ["./webapp"]
