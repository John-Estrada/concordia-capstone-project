import React, { useEffect } from "react";
import { useState, useRef } from "react";

const wrapperStyle = {
  border: "1px solid black",
  minWidth: "35em",
  padding: "1em",
  display: "flex",
  justifyContent: "space-around",
};
const outer = {};

const resultsStyle = {
  marginTop: "1em",
  display: "flex",
  flexDirection: "column",
};

const selectorButtonStyle = {
  padding: "0.5em",
  borderRadius: "6px",
  cursor: "pointer",
};

const selectedStyle = {
  border: '1px solid black',
  backgroundColor: "white",
  color: "black",
  borderRadius: "6px",
};

const notSelectedStyle = {
  border: '1px solid black',
  backgroundColor: "black",
  color: "white",
  borderRadius: '6px'
};

const DataPanel = (props) => {
  const baseUrl = "http://localhost:8000/api/";
  const [availableDataTypes, setAvailableDataTypes] = useState([]);
  const [selectedDataType, setSelectedDataType] = useState(null);
  const [displayString, setDisplayString] = useState([]);

  const resultsGoHere = useRef(null);

  const selectType = (e) => {
    console.log(e.target.innerHTML);
    setSelectedDataType(e.target.innerHTML);
  };

  useEffect(() => {
    fetch(baseUrl + `controller_has_data?controller=${props.controllerName}`)
      .then((res) => res.json())
      .then((res) => {
        console.log(`data types: ${res.data_types}`);
        if (res.data_types != undefined && res.data_types.length > 0) {
          setAvailableDataTypes(res.data_types);
        } else {
          setAvailableDataTypes([]);
        }
      });
  }, [props.controllerName]);

  useEffect(() => {
    if (selectedDataType == null) return;

    let requestUrl =
      baseUrl +
      `generic?controller=${
        props.controllerName
      }&sensor=${selectedDataType}&start=111&end=${Math.round(
        new Date().getTime() / 1000
      )}`;
    console.log(requestUrl);
    fetch(requestUrl)
      .then((res) => res.json())
      .then((res) => {
        console.log(res.results);
        let dataMap = new Map();
        res.results.forEach((result) => {
          let date = result[0].split("T")[0];
          let time = result[0].split("T")[1];
          let value = result[1];

          console.log(`date: ${date}, time: ${time}, value: ${value}`);
          if (!dataMap.has(date)) {
            dataMap.set(date, []);
          }

          dataMap.get(date).push({ time, value });
        });
        resultsGoHere.current.innerHTML = "";

        dataMap.forEach((value, key) => {
          let day = document.createElement("div");
          let text = document.createTextNode(key);

          day.appendChild(text);
          resultsGoHere.current.appendChild(day);

          value.forEach((v) => {
            let time = v.time;
            let dataEntry = v.value;
            let line = document.createElement("div");
            let t = document.createTextNode(`${time.split('.')[0]} - ${dataEntry}`);
            line.appendChild(t);

            resultsGoHere.current.appendChild(line);
          });

          let lineBreak = document.createElement("br");
          resultsGoHere.current.appendChild(lineBreak);
        });
      });
  }, [selectedDataType, props.controllerName]);

  return (
    <div style={outer}>
      <div style={wrapperStyle}>
        {availableDataTypes.length == 0 ? (
          <div>No Data Available</div>
        ) : (
          availableDataTypes.map((type) => {
            return (
              <div
                style={
                  type != selectedDataType ? selectedStyle : notSelectedStyle
                }
              >
                <div onClick={selectType} style={selectorButtonStyle}>
                  {type}
                </div>
              </div>
            );
          })
        )}
      </div>
      <div style={resultsStyle} ref={resultsGoHere}></div>
    </div>
  );
};

export default DataPanel;
