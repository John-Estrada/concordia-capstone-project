import React from "react";
import Button from "./Button";
import ControllerThumbnailCard from "./ControllerThumbnailCard";
import AddControllerDialogBox from "./AddControllerDialogBox";
import { useState, useEffect, useRef } from "react";
import axios from "axios";
import Ripples from "react-ripples";

const container = {
  width: "256px",
  borderRadius: "8px",
  margin: "auto",
  backgroundColor: "white",
  paddingLeft: "32px",
  paddingRight: "32px",
  display: "flex",
  flexDirection: "column",
  gap: "16px",
  paddingBottom: "16px",
  paddingTop: "16px",
  overflowY: "scroll",
  maxHeight: "512px",
};

const topBar = {
  display: "flex",
  gap: "10px",
  paddingLeft: "10px",
};

const titleStyle = {
  fontSize: 24,
  margin: "8px",
};

const thumbnailCardsContainer = {
  display: "flex",
  flexDirection: "column",
  gap: "10px",
};

const lowerButtonsContainer = {
  display: "flex",
  flexDirection: "row",
  justifyContent: "flex-end",
  gap: "0.75em",
};

function ControllerSelectionBox(props) {
  const baseUrl = `http://${process.env.REACT_APP_URL}:8000/api/get_available_controllers`;

  const [addControllerPopupOpen, setAddControllerPopupOpen] = useState(false);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [controllerAddIndicator, setControllerAddIndicator] = useState(0); //for useEffect to render when a new controller is added

  const togglePopupButton = useRef(null);
  const popupWrapper = useRef(null);

  let popupWrapperStyle = {
    position: "absolute",
    top: `${mousePos.y + 12}px`,
    left: `${mousePos.x + 12}px`,
  };

  const toggleAddControllerPopup = (e) => {
    setAddControllerPopupOpen(!addControllerPopupOpen);
    setMousePos({ x: e.pageX, y: e.pageY });
    console.log(mousePos);
  };

  //allow child components to trigger a new render via useEffect whenever a controller is added
  const signalAddController = (index) => {
    setControllerAddIndicator(controllerAddIndicator + 1);
  };

  // const [selectedController, setSelectedController] = useState(1);  //TODO: fix this - handle no controllers yet
  const [allControllers, setAllControllers] = useState([
    { id: -1, name: "debug", selected: "false" },
  ]);

  const refreshControllers = () => {
    console.log("refreshing");
    axios.get(baseUrl).then((res) => {
      console.log(res.data.controllers);
      let all = [];

      res.data.controllers.forEach((controller) => {
        all.push({
          id: controller[0],
          name: controller[1],
          selected: "false",
        });
      });

      setAllControllers(all);
    });
  };

  useEffect(() => {
    refreshControllers();
  }, [controllerAddIndicator]);

  return (
    <div>
      <div style={titleStyle}>Controllers</div>
      <div style={container}>
        <div style={topBar}>
          <div>ID</div>
          <div>Name</div>
        </div>
        <div id="thumbnailCardsContainer" style={thumbnailCardsContainer}>
          {allControllers.map((item) => {
            return (
              <ControllerThumbnailCard
                id={item.id}
                name={item.name}
                selected={
                  item.id === props.selectedController ? "true" : "false"
                }
                key={item.id}
                handleClick={() => {
                  props.sendSelectedControllerToParent(item.id);
                  console.log(`Controller number ${item.id} selected`);
                }}
              />
            );
          })}
        </div>
        <div style={lowerButtonsContainer}>
          <Ripples color="#fff" during={500}>
            <Button
              icon="refresh"
              text="refresh"
              handleClick={() => {
                refreshControllers();
              }}
            />
          </Ripples>
          <Ripples color="#fff" during={500}>
            <Button
              icon="add"
              text="add"
              ref={togglePopupButton}
              handleClick={toggleAddControllerPopup}
            />
          </Ripples>
        </div>
        {addControllerPopupOpen && (
          <div ref={popupWrapper} style={popupWrapperStyle}>
            <AddControllerDialogBox
              handleCancel={toggleAddControllerPopup}
              signalAddController={signalAddController}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default ControllerSelectionBox;
