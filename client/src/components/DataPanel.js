import React, { useEffect } from "react";
import { useState, useRef } from "react";
import TimeSelectPanel from "./TimeSelectPanel";

const wrapperStyle = {
  border: "1px solid black",
  minWidth: "35em",
  maxWidth: "50vw",
  padding: "1em",
  margin: "0.5em",
  display: "flex",
  justifyContent: "center",
  flexWrap: "wrap",
  gap: '0.125em'
};
const outer = {};

const resultsStyle = {
  marginTop: "1em",
  display: "flex",
  flexDirection: "column",
  overflow: "scroll",
};

const selectorButtonStyle = {
  padding: "0.5em",
  borderRadius: "6px",
  cursor: "pointer",
};

const selectedStyle = {
  border: "1px solid black",
  backgroundColor: "white",
  color: "black",
  borderRadius: "6px",
};

const notSelectedStyle = {
  border: "1px solid black",
  backgroundColor: "black",
  color: "white",
  borderRadius: "6px",
};

const timeAndDataWrapper = {
  display: "flex",
};

const DataPanel = (props) => {
  const baseUrl = `http://${process.env.REACT_APP_URL}/api/`;
  const [availableDataTypes, setAvailableDataTypes] = useState([]);
  const [selectedDataType, setSelectedDataType] = useState(null);

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
      <div style={timeAndDataWrapper}>
        <TimeSelectPanel
          controllerName={props.controllerName}
          selectedDataType={selectedDataType}
        ></TimeSelectPanel>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            flex: "1",
            justifyContent: "center",
          }}
        >
        </div>
      </div>
    </div>
  );
};

export default DataPanel;
