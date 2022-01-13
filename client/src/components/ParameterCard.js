import React from "react";
import "../App.css";
import Button from "./Button";
import axios from "axios";
import SharedStyles from "./SharedStyles";
import { GiConsoleController } from "react-icons/gi";
import Ripples from "react-ripples";

const container = {
  width: "264px",
  borderRadius: "8px",
  margin: "auto",
  backgroundColor: "white",
  paddingLeft: "32px",
  paddingRight: "32px",
  display: "flex",
  flexDirection: "column",
  gap: "16px",
  paddingBottom: "16px",
};

const resultsStyle = {
  display: "flex",
  flexDirection: "column",
  gap: "8px",
};

const maxAvgMinContainer = {
  display: "flex",
  flexDirection: "row",
  width: "172px",
  margin: "auto",
  // border: "1px solid black",
  justifyContent: "space-around",
  gap: "24px",
};

const maxAvgMin = {
  display: "flex",
  flexDirection: "column",
};

const dateSelectorContainer = {
  display: "flex",
  flexDirection: "column",
  justifyContent: "space-around",
  alignItems: "flex-start",
  margin: "auto",
  width: "100%",
  gap: "10px",
  padding: "2px",
};

const dateSelector = {
  display: "flex",
  flexDirection: "column",
  justifyContent: "space-between",
  width: "100%",
};

function ParameterCard(props) {
  const baseUrl = "http://localhost:8000/api/generic"; //TODO put this in its own file, change to better url

  const [max, setMax] = React.useState(-999999);
  const [avg, setAvg] = React.useState(-999999);
  const [min, setMin] = React.useState(-999999);

  const [results, setResults] = React.useState(
    "Select a time range to view the results"
  );

  const outPutDiv = React.useRef(null);

  const dateSelectorFrom = React.useRef(null);
  const timeSelectorFrom = React.useRef(null);

  const dateSelectorTo = React.useRef(null);
  const timeSelectorTo = React.useRef(null);

  React.useEffect(() => {
    setMax(-999999);
    setMin(-999999);
    setAvg(-999999);
    outPutDiv.current.innerHTML = "";
  }, [props.selectedController]);

  const fetchDataHandler = () => {
    let startDate = new Date(dateSelectorFrom.current.value).getTime() / 1000;
    let startTime = timeSelectorFrom.current.value;
    let startHours = startTime.split(":")[0];
    let startMinutes = startTime.split(":")[1];
    let startTimeStamp =
      startDate +
      parseInt(startHours) * 1000 * 60 +
      parseInt(startMinutes) * 1000;

    let start = startTimeStamp;
    let end = 9999999999; //TODO get actual end date

    console.log(`${start}, ${startTimeStamp}`);
    if (isNaN(start)) {
      setResults("Please enter a date and time in every field");
      return;
    }

    axios
      .get(baseUrl, {
        params: {
          sensor: `${props.sensor}`,
          start: start,
          end: end,
          controller: props.selectedController,
        },
      })
      .then((response) => {
        if (response.data.results.length < 1) {
          setResults("No data found");
          outPutDiv.current.innerHTML = "No data found";
        } else {
          let resDict = {};
          response.data.results.forEach((result) => {
            let date = result[0].split("T")[0];
            if (!resDict[date]) {
              resDict[date] = [];
            }

            resDict[date].push({
              time: result[0].split("T")[1].slice(0, -1),
              value: result[1],
            });
          });

          let outputString = "";

          outPutDiv.current.innerHTML = "";

          let count = 0;
          let total = 0;
          let minCompare = 999999999; //needed to avoid setState not updating until after async event

          Object.keys(resDict).forEach((key) => {
            console.log("a");
            outPutDiv.current.innerHTML = `${outPutDiv.current.innerHTML}<div>${key}<div>`;

            resDict[key].forEach((result) => {
              console.log("b");
              count += 1;
              total += parseFloat(result.value);
              setAvg((total / count).toFixed(2));

              if (parseFloat(result.value) > max) {
                setMax(result.value);
              }

              console.log(`c : ${result.value}, min: ${minCompare}`);
              if (parseFloat(result.value) < minCompare) {
                console.log("e");
                setMin(result.value);
                minCompare = result.value;
                console.log(`min: ${min}`);
              }
              console.log("d");

              console.log(result.value);

              let c = document.createElement("div");
              c.style = "display: flex; justify-content: center; gap: 2em";
              c.innerHTML = `<div>${result.time}</div> <div>${result.value}</div>`;
              outPutDiv.current.append(c);
            });
          });

          setResults(outputString);
        }
      });
  };

  return (
    <div style={container}>
      <div style={SharedStyles.titleStyle}>{props.title}</div>
      <div style={maxAvgMinContainer}>
        <div style={maxAvgMin}>
          <div>Max</div>
          <div>{max === -999999 ? "..." : max}</div>
        </div>
        <div style={maxAvgMin}>
          <div>Avg</div>
          <div>{avg === -999999 ? "..." : avg}</div>
        </div>
        <div style={maxAvgMin}>
          <div>Min</div>
          <div>{min === -999999 ? "..." : min}</div>
        </div>
      </div>
      <div style={dateSelectorContainer}>
        <div style={dateSelector}>
          <div style={{ textAlign: "left", marginLeft: "0.75em" }}>From</div>
          <div>
            <input type="date" ref={dateSelectorFrom}></input>
            <input type="time" ref={timeSelectorFrom}></input>
          </div>
        </div>
      </div>
      <div style={dateSelectorContainer}>
        <div style={dateSelector}>
          <div style={{ textAlign: "left", marginLeft: "0.75em" }}>To</div>
          <div>
            <input type="date" ref={dateSelectorTo}></input>
            <input type="time" ref={timeSelectorTo}></input>
          </div>
        </div>
      </div>
      <div>
        <Ripples color="#fff" during={500} style={{ backgroundColor: "blue" }}>
          <Button text="go" handleClick={fetchDataHandler}></Button>
        </Ripples>
      </div>
      <div ref={outPutDiv} style={resultsStyle}></div>
      {results}
    </div>
  );
}

export default ParameterCard;
