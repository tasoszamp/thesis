FROM alpine

WORKDIR /app
ADD dist/sensor_data .
ADD dist/sensor_sub .
ADD dataset.json .

CMD ./sensor_sub