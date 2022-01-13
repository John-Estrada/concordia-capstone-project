import React from "react";
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
        <div>
          <ParameterCard
            title="Temperature (C)"
            selectedController={props.selectedController}
            sensor={"temperature"}
          />
        </div>
        <div>
          <ParameterCard
            title="Humidity"
            selectedController={props.selectedController}
            sensor={"humidity"}
          />
        </div>
        <div>
          <ParameterCard
            title="pH"
            selectedController={props.selectedController}
            sensor={"ph"}
          />
        </div>
        <div>
          <ParameterCard
            title="Conductivity"
            selectedController={props.selectedController}
            sensor={"conductivity"}
          />
        </div>
        <div>
          <ParameterCard
            title="Flow Rate"
            selectedController={props.selectedController}
            sensor={"flow"}
          />
        </div>
      </div>
    </div>
  );
}

export default RightPanel;
