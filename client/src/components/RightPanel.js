import React from "react";
import DataPanel from "./DataPanel";
import ParameterCard from "./ParameterCard";
import SharedStyles from "./SharedStyles";

const container = {
  display: "flex",
  flexDirection: "row",
  justifyContent: "left",
  gap: "0.5em",
  margin: "8px",
};

function RightPanel(props) {
  return (
    <div>
      <div style={SharedStyles.titleStyle}>{props.title}</div>
      <div style={container}>
        <DataPanel
          selectedController={props.selectedController}
          controllerName={props.controllername}
        ></DataPanel>
      </div>
    </div>
  );
}

export default RightPanel;
