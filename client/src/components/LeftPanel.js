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
      />
      <div style={verticalSpacer}></div>
      <ControllerDetailCard
        title="Controller detail card"
        selectedController={props.selectedController}
      />
    </div>
  );
}

export default LeftPanel;
