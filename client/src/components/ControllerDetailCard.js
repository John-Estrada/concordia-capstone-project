import React from "react";
import Button from "./Button";
import styled from "styled-components";
import axios from "axios";
import Ripples from "react-ripples";
import AddTargetDialog from "./AddTargetDialog";

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
};

const titleStyle = {
  fontSize: 24,
  margin: "8px",
};

const rows = {
  display: "flex",
  flexDirection: "column",
  gap: "20px",
};

const rightSideOfRowStyle = {
  display: "flex",
  flexDirection: "row",
  alignItems: "center",
  gap: "16px",
};

const targetSelectorStyle = {
  width: "32px",
  border: "0",
  outline: "0",
  background: "transparent",
  borderBottom: "1px solid black",
};

const lowerButtonsContainer = {
  display: "flex",
  flexDirection: "row",
  justifyContent: "flex-end",
  gap: "0.75em",
};

const StyledRow = styled.div`
  display: flex;
  flex-direction: row;
  width: 100%;
  align-items: center;
  justify-content: space-between;
`;

//TODO clean up this type of styling
const Row = (props) => {
  const baseUrl = `http://${process.env.REACT_APP_URL}:8000/api/target`;
  const [target, setTarget] = React.useState(props.defaultValue);
  const [buttonDisabled, setButtonDisabled] = React.useState(true);
  const targetSelector = React.useRef(null);

  const handleChangeTarget = (e) => {
    setButtonDisabled(true);
    if (
      targetSelector.current.value != undefined &&
      targetSelector.current.value != null &&
      targetSelector.current.value != ""
    ) {
      setTarget(targetSelector.current.value); //note - target does not update until after this function is finished

      let params = new URLSearchParams();

      params.append("id", props.selectedController);
      params.append("target", targetSelector.current.value); //note - setTarget will not update until this function is finished
      params.append("name", props.rowTitle);

      axios.post(baseUrl, params); //TODO: error handling

      targetSelector.current.value = ""; //cleanup after the request so we can have the value
    }

    targetSelector.current.style.backgroundColor = "white";
    targetSelector.current.style.borderBottom = "1px solid black";
  };

  return (
    <StyledRow>
      <div>{props.rowTitle}</div>
      <div style={rightSideOfRowStyle}>
        <input
          ref={targetSelector}
          placeholder={target}
          style={targetSelectorStyle}
          onFocus={(e) => {
            e.target.style.borderBottom = "2px solid black";
            e.target.style.backgroundColor = "#e5e5e5";
            setButtonDisabled(false);
          }}
        ></input>
        <div>
          <Button
            text="confirm"
            handleClick={handleChangeTarget}
            disabled={buttonDisabled}
          ></Button>
        </div>
      </div>
    </StyledRow>
  );
};

function ControllerDetailCard(props) {
  const [targets, setTargets] = React.useState([]);
  const [addTargetDialogOpen, setAddTargetDialogOpen] = React.useState(false);
  const [mousePos, setMousePos] = React.useState({ x: 0, y: 0 });
  const [refreshTrigger, setRefreshTrigger] = React.useState(1)

  const baseUrl = `http://${process.env.REACT_APP_URL}/api/all_targets`;
  const params = { controller: props.controllerName };

  let popupWrapperStyle = {
    position: "absolute",
    top: `${mousePos.y + 12}px`,
    left: `${mousePos.x + 12}px`,
  };

  const closeDialogBox = () => {
    setAddTargetDialogOpen(false);
    setRefreshTrigger(refreshTrigger+1)
  };

  const refreshTargets = () => {
    axios.get(baseUrl, { params }).then((res) => {
      let results = res.data.results;
      let output = [];
      for (const property in results) {
        console.log(property);
        console.log(results[property]);
        // setTargets([property])
        output.push({ property: property, target: results[property] });
      }
      setTargets(output);
    });
  };

  const handleDeleteTarget = (targetType) => {
    console.log(targetType);
    const requestUrl = `http://${process.env.REACT_APP_URL}/api/remove_target`;
    const requestParams = new URLSearchParams();
    requestParams.append("type", targetType);
    requestParams.append("controller", props.controllerName);

    axios.post(requestUrl, requestParams).then((res) => {
      console.log(res);
    });
    setRefreshTrigger(refreshTrigger+1)
  };

  React.useEffect(() => {
    if (props.selectedController === -1) return;
    refreshTargets();
  }, [props.selectedController, refreshTrigger],);

  return (
    <div>
      <div style={container}>
        {props.selectedController == -1 ? (
          <div style={titleStyle}>No Controller Selected</div>
        ) : (
          <>
            <div
              style={titleStyle}
            >{`Controller ${props.selectedController}`}</div>
            <div style={rows}>
              {targets.map((target) => {
                return (
                  <div
                    style={{
                      display: "flex",
                      gap: "16px",
                      justifyContent: "flex-end",
                      alignItems: "center",
                    }}
                  >
                    <div style={{ marginLeft: "0px", marginRight: "auto" }}>
                      {target.property}
                    </div>
                    <div>{target.target}</div>
                    <Button
                      text="remove"
                      icon="cancel"
                      handleClick={() => {
                        console.log("clicked");
                        handleDeleteTarget(target.property);
                      }}
                    ></Button>
                  </div>
                );
              })}
            </div>
            <div style={lowerButtonsContainer}>
              <Ripples during={500} color="#fff" onClick={refreshTargets}>
                <Button text="refresh" icon="refresh"></Button>
              </Ripples>
              <Ripples
                during={500}
                color="#fff"
                onClick={(e) => {
                  setAddTargetDialogOpen(true);
                  setMousePos({ x: e.pageX, y: e.pageY });
                }}
              >
                <Button text="add" icon="add"></Button>
              </Ripples>
              {addTargetDialogOpen ? (
                <div style={popupWrapperStyle}>
                  <AddTargetDialog
                    handleCancel={closeDialogBox}
                    controllerName={props.controllerName}
                    handleRefresh={refreshTargets}
                  ></AddTargetDialog>
                </div>
              ) : null}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default ControllerDetailCard;
