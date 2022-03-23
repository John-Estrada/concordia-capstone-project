import React from "react";
import "../App.css";
import axios from "axios";
import Button from "./Button";
import Ripples from "react-ripples";

const timePanelStyle = {
  padding: "1em",

  minWidth: "15em",
  maxWidth: "75vw",
};

const resultsPanel = {
  minWidth: "30em",
  maxWidth: "30em",
  border: "1px solid black",
  padding: "0.5em",
  margin: "0.25em",
  overflow: "scroll",
};

const TimeSelectPanel = (props) => {
  const url = `http://${process.env.REACT_APP_URL}/api/generic`;
  const [selectedTime, setSelectedTime] = React.useState("hour");
  const [req, setReq] = React.useState("none");
  const [results, setResults] = React.useState([]);

  let timeOptions = [
    "hour",
    "6 hours",
    "12 hours",
    "day",
    "week",
    "month",
    "all",
  ];

  const handleRequestData = () => {
    if (!props.controllerName) return;
    let now = new Date();
    let begin = new Date();
    switch (selectedTime) {
      case "hour":
        begin.setHours(now.getHours() - 1);
        break;
      case "6 hours":
        begin.setHours(now.getHours() - 6);
        break;
      case "12 hours":
        begin.setHours(now.getHours() - 12);
        break;
      case "day":
        begin.setHours(now.getHours() - 24);
        break;
      case "week":
        begin.setDate(now.getDate() - 7);
        break;
      case "month":
        begin.setMonth(now.getMonth() - 1);
        break;
      case "all":
        begin.setFullYear(2000);
        break;
      default:
        begin.setHours(now.getHours() - 1);
        break;
    }
    setReq(begin.getTime());

    const params = new URLSearchParams();
    params.append("controller", props.controllerName);
    params.append("start", Math.round(begin.getTime() / 1000));
    params.append("end", Math.round(now.getTime() / 1000));
    params.append("sensor", props.selectedDataType);

    axios
      .get(url, { params })
      .then((res) => {
        console.log(res.data.results);
        if (res.data.results === "This controller does not exist") return;

        let output = [];
        res.data.results.forEach((result) => {
          let date = result[0].split('.')[0]
          let value = result[1]
          output.push(`${date} - ${value}`);
        });
        setResults(output);
      })
      .catch((err) => console.log(err));
  };

  const handleDownloadCsv = () => {
    console.log("download");
    if (!props.controllerName) return;
    let now = new Date();
    let begin = new Date();
    switch (selectedTime) {
      case "hour":
        begin.setHours(now.getHours() - 1);
        break;
      case "6 hours":
        begin.setHours(now.getHours() - 6);
        break;
      case "12 hours":
        begin.setHours(now.getHours() - 12);
        break;
      case "day":
        begin.setHours(now.getHours() - 24);
        break;
      case "week":
        begin.setDate(now.getDate() - 7);
        break;
      case "month":
        begin.setMonth(now.getMonth() - 1);
        break;
      case "all":
        begin.setFullYear(2000);
        break;
      default:
        begin.setHours(now.getHours() - 1);
        break;
    }

    const requestUrl = `http://${process.env.REACT_APP_URL}/api/get_data_as_csv?controller=${props.controllerName}&sensor=${props.selectedDataType}&start=${Math.round(begin.getTime() / 1000)}&end=${Math.round(now.getTime() / 1000)}`;
    window.open(requestUrl)
  };

  React.useEffect(() => {
    handleRequestData();
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
                {option}
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
            style={{ marginTop: "0.25em" }}
            onClick={handleDownloadCsv}
          >
            <Button text="download"></Button>
          </Ripples>
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
        <div>
          {results.length > 0 ? null : "No Results Found"}{" "}
          {results.map((result) => {
            return <div>{result.replace("T", " ").replace("Z", " ")}</div>;
          })}
        </div>
      </div>
    </div>
  );
};

export default TimeSelectPanel;
