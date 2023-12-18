FROM alpine

WORKDIR /app
ADD dist/sensor_data .
ADD dist/sensor_sub .
ADD dist/set_startpoint .
ADD dataset.json .

CMD ./set_startpoint && ./sensor_sub