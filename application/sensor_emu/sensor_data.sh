#!/bin/bash

NumOfMetrics=$(jq length ../dataset/AirQuality.json)

Randomizer=$(( $RANDOM % $NumOfMetrics + 1 ))

cat ../dataset/AirQuality.json | jq " .\"$Randomizer\""