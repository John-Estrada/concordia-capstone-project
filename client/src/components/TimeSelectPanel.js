import React from "react";
import "../App.css";
import axios from "axios";
import Button from "./Button";
import Ripples from "react-ripples";
import { BsFileBreakFill } from "react-icons/bs";

let disabledText =
  " Data preview for this option has been disabled to save server bandwidth - if you want to see the data, click the download button on the left";

let controlParameters = ["vent", "peltier", "pump", "top_tank", "bottom_tank"];

const timePanelStyle = {
  padding: "1em",

  minWidth: "14em",
  maxWidth: "75vw",
};

const resultsPanel = {
  minWidth: "15em",
  maxWidth: "30em",
  border: "1px solid black",
  padding: "0.5em",
  margin: "0.25em",
  overflow: "scroll",
  overflowY: "scroll",
  maxHeight: "30em",
};

const averagesPanel = {};

function toIsoString(date) {
  var tzo = -date.getTimezoneOffset(),
    dif = tzo >= 0 ? "+" : "-",
    pad = function (num) {
      return (num < 10 ? "0" : "") + num;
    };

  return (
    date.getFullYear() +
    "-" +
    pad(date.getMonth() + 1) +
    "-" +
    pad(date.getDate()) +
    "T" +
    pad(date.getHours()) +
    ":" +
    pad(date.getMinutes()) +
    ":" +
    pad(date.getSeconds()) +
    dif +
    pad(Math.floor(Math.abs(tzo) / 60)) +
    ":" +
    pad(Math.abs(tzo) % 60)
  );
}

const TimeSelectPanel = (props) => {
  const url = `http://${process.env.REACT_APP_URL}/api/generic`;
  const avgUrl = `http://${process.env.REACT_APP_URL}/api/hourly_average`;
  const controlSystemUrl = `http://${process.env.REACT_APP_URL}/api/control_systems_activity`;
  const [selectedTime, setSelectedTime] = React.useState("hour");
  const [req, setReq] = React.useState("none");
  const [results, setResults] = React.useState([]);
  const [averages, setAverages] = React.useState([]);
  const [controlLog, setControlLog] = React.useState([]);

  let timeOptions = [
    "minute",
    "hour",
    "6 hours",
    "12 hours",
    "today",
    "yesterday",
    "week",
    "month",
    "all",
  ];

  const getDateFromTimeChoice = () => {
    let now = new Date();
    let begin = new Date();
    switch (selectedTime) {
      case "minute":
        begin.setMinutes(now.getMinutes() - 1);
        break;
      case "hour":
        begin.setHours(now.getHours() - 1);
        break;
      case "6 hours":
        begin.setHours(now.getHours() - 6);
        break;
      case "12 hours":
        begin.setHours(now.getHours() - 12);
        break;
      case "today":
        begin.setHours(0);
        break;
      case "yesterday":
        begin.setDate(begin.getDate() - 1);
        begin.setHours(0);
        now.setHours(0);
        break;
      case "week":
        begin.setDate(now.getDate() - 7);
        setResults([disabledText]);
        break;
      case "month":
        begin.setMonth(now.getMonth() - 1);
        setResults([disabledText]);
        break;
      case "all":
        begin.setFullYear(2000);
        setResults([disabledText]);
        break;
      default:
        begin.setHours(now.getHours() - 1);
        break;
    }

    return { begin, now };
  };

  const handleRequestData = () => {
    if (!props.controllerName) return;

    let dates = getDateFromTimeChoice();

    console.log(`${dates.now}, ${dates.begin}`);

    if (
      selectedTime === "all" ||
      selectedTime === "week" ||
      selectedTime === "month"
    ) {
      setResults([disabledText]);
      return;
    }

    const params = new URLSearchParams();
    params.append("controller", props.controllerName);
    params.append("start", Math.round(dates.begin.getTime() / 1000));
    params.append("end", Math.round(dates.now.getTime() / 1000));
    params.append("sensor", props.selectedDataType);
    params.append("data_type", props.selectedDataType);

    axios
      .get(url, { params })
      .then((res) => {
        console.log(res.data.results);
        if (res.data.results === "This controller does not exist") return;
        if (!res.data.results) return;

        let output = [];
        res.data.results.forEach((result) => {
          let date = new Date(result[0] * 1000);
          let value = result[1];
          output.push(
            `${toIsoString(date).substring(
              0,
              toIsoString(date).length - 6
            )} - ${value}`
          );
        });
        setResults(output);
      })
      .catch((err) => console.log(err));

    if (controlParameters.includes(props.selectedDataType)) {
      setAverages(["a", "b"]);
      return;
    }

    axios.get(avgUrl, { params }).then((res) => {
      if (res.data.results === "This controller does not exist") return;
      console.log(res.data.averages);
      let output = [];
      res.data.averages.forEach((avg) => {
        output.push(avg);
      });
      setAverages(output);
    });
  };

  const handleDownloadCsv = () => {
    if (!props.controllerName) return;

    let dates = getDateFromTimeChoice();

    const requestUrl = `http://${
      process.env.REACT_APP_URL
    }/api/get_data_as_csv?controller=${props.controllerName}&sensor=${
      props.selectedDataType
    }&start=${Math.round(dates.begin.getTime() / 1000)}&end=${Math.round(
      dates.now.getTime() / 1000
    )}`;
    window.open(requestUrl);
  };

  const getAveragesAsCsv = () => {
    if (!props.controllerName) return;

    let dates = getDateFromTimeChoice();
    const requestUrl = `http://${
      process.env.REACT_APP_URL
    }/api/get_averages_as_csv?controller=${props.controllerName}&data_type=${
      props.selectedDataType
    }&start=${Math.round(dates.begin.getTime() / 1000)}&end=${Math.round(
      dates.now.getTime() / 1000
    )}`;
    window.open(requestUrl);
  };

  const handleControlSystemStatus = () => {
    setControlLog([]);
    if (!props.controllerName) return;
    if (!controlParameters.includes(props.selectedDataType)) return;
    let dates = getDateFromTimeChoice();

    const params = new URLSearchParams();
    params.append("controller", props.controllerName);
    // params.append("start", Math.round(dates.begin.getTime() / 1000));
    // params.append("end", Math.round(dates.now.getTime() / 1000));
    params.append("data_type", props.selectedDataType);

    axios.get(controlSystemUrl, { params }).then((res) => {
      if (!res.data.results) return;
      console.log(res.data.results);
      let output = [];
      res.data.results.forEach((result) => {
        let date = new Date(parseInt(result) * 1000);
        let datePieces = date.toISOString().split("T");
        let days = datePieces[0];
        let hours = datePieces[1].split(".")[0];

        output.push(`${days} ${hours}`);
      });
      setControlLog(output);
    });
  };

  React.useEffect(() => {
    handleRequestData();
    handleControlSystemStatus();
  }, [props.controllerName, selectedTime, props.selectedDataType]);

  return (
    <div style={{ display: "flex" }}>
      <div style={timePanelStyle}>
        <div>Select Time Range</div>
        <div>
          {timeOptions.map((option) => {
            return (
              <div
                className={
                  option === selectedTime
                    ? "button-selected"
                    : "button-not-selected"
                }
                onClick={(e) => {
                  e.target.className = "button-selected";
                  setSelectedTime(option);
                }}
              >
                {option === "today"
                  ? `today (${new Date().getFullYear()}-${
                      new Date().getMonth() + 1
                    }-${new Date().getDate()})`
                  : null}
                {option === "yesterday"
                  ? `yesterday (${new Date().getFullYear()}-${
                      new Date().getMonth() + 1
                    }-${new Date().getDate() - 1})`
                  : null}
                {option != "today" && option != "yesterday" ? option : null}
              </div>
            );
          })}
        </div>
        <div
          style={{ display: "flex", justifyContent: "flex-end", gap: "10px" }}
        >
          <Ripples
            color="#fff"
            during={500}
            onClick={handleRequestData}
            style={{ marginTop: "0.25em" }}
          >
            <Button text="refresh" icon="refresh"></Button>
          </Ripples>
        </div>
      </div>
      <div style={resultsPanel}>
        <div>
          {props.controllerName} | {selectedTime} | {props.selectedDataType}
        </div>
        <p></p>
        <Ripples
          color="#fff"
          during={500}
          style={{ marginTop: "0.25em" }}
          onClick={handleDownloadCsv}
        >
          <Button text="download" icon="csv"></Button>
        </Ripples>
        <div style={{ overflow: "scroll" }}>
          <p></p>
          {results.length > 0 ? null : "No Results Found"}{" "}
          {results.map((result) => {
            return <div>{result.replace("T", " ").replace("Z", " ")}</div>;
          })}
        </div>
      </div>
      <div style={resultsPanel}>
        <div>
          {!controlParameters.includes(props.selectedDataType) ? (
            <div>
              <div>Hourly Averages</div>
              <p></p>
              <Ripples during={500} color="#fff" onClick={getAveragesAsCsv}>
                <Button text="download" icon="csv"></Button>
              </Ripples>
            </div>
          ) : (
            "Times active"
          )}
        </div>
        <p></p>
        <div>
          {averages.length > 0 ? null : "No averages found"}{" "}
          {averages.length > 0 &&
          !controlParameters.includes(props.selectedDataType)
            ? averages.map((avg) => {
                let x = new Date(avg[0] * 1000);
                let stringDate = toIsoString(x).split("T")[0];
                let stringTime = toIsoString(x).split("T")[1].split("-")[0];
                return (
                  <div>
                    {`${stringDate} ${stringTime}`} -{" "}
                    {parseFloat(avg[1]).toFixed(2)}
                  </div>
                );
              })
            : null}
          <div>
            {controlLog.length > 0
              ? controlLog.map((item) => {
                  return <div>{item}</div>;
                })
              : null}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TimeSelectPanel;
