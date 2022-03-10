import logo from "./logo.svg";
import "./App.css";
import ParameterCard from "./components/ParameterCard";
import Button from "./components/Button";
import ControllerSelectionBox from "./components/ControllerSelectionBox";
import RightPanel from "./components/RightPanel";
import LeftPanel from "./components/LeftPanel";
import TestComponent from "./components/TestComponent";
import TestParent from "./components/TestParent";
import { useState, useRef } from "react";
import AddControllerDialogBox from "./components/AddControllerDialogBox";
import TestChild from "./components/TestChild";

const container = {
  display: "flex",
  flexDirection: "row",
  padding: "16px",
};

function App() {
  const [selectedController, setSelectedController] = useState(-1); //TODO use name instead of id, randomize new controller id
  const [controllerName, setControllerName] = useState(
    "No Controller Selected"
  );

  //callback for child components
  const sendSelectedControllerToParent = (controllerId) => {
    setSelectedController(controllerId);
  };

  const sendNameToParent = (controllerName) => {
    setControllerName(controllerName);
  };

  return (
    <div className="App">
      <div style={container}>
        <LeftPanel
          selectedController={selectedController}
          sendSelectedControllerToParent={sendSelectedControllerToParent}
          sendNameToParent={sendNameToParent}
        />
        <RightPanel
          title={
            selectedController === -1
              ? "No Controller Selected"
              : "Controller " + selectedController
          }
          selectedController={selectedController}
          controllername={controllerName}
        />
      </div>
    </div>
  );
}

export default App;
