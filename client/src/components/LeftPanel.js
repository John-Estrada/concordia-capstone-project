import React from "react";
import ControllerDetailCard from "./ControllerDetailCard";
import ControllerSelectionBox from "./ControllerSelectionBox";

const verticalSpacer = {
  height: "1em",
};

function LeftPanel(props) {
  return (
    <div>
      <ControllerSelectionBox
        selectedController={props.selectedController}
        sendSelectedControllerToParent={props.sendSelectedControllerToParent}
        sendNameToParent = {props.sendNameToParent}
        controllerName = {props.controllerName}
      />
      <div style={verticalSpacer}></div>
      <ControllerDetailCard
        title="Controller detail card"
        selectedController={props.selectedController}
        controllerName = {props.controllerName}
      />
    </div>
  );
}

export default LeftPanel;
