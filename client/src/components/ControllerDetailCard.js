import React from "react";
import Button from "./Button";
import styled from "styled-components";
import axios from "axios";

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
  const [devices, setDevices] = React.useState([]);
  const baseUrl = `http://${process.env.REACT_APP_URL}:8000/api/target`;
  const params = { id: props.selectedController };

  React.useEffect(() => {
    if (props.selectedController === -1) return;
    axios.get(baseUrl, { params }).then((res) => {
      let results = [];
      //create an array of the devices
      res.data.devices.forEach((device) => {
        results.push(device);
      });

      setDevices(results);
    });
  }, [props.selectedController]);

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
              {devices.map((device) => {
                return (
                  <Row
                    rowTitle={device.name}
                    defaultValue={device.target}
                    selectedController={props.selectedController}
                  />
                );
              })}
              {/* <Row rowTitle="Temperature" defaultValue={22.2}></Row>
              <Row rowTitle="Humidity"></Row>
              <Row rowTitle="pH"></Row>
              <Row rowTitle="Conductivity"></Row>
              <Row rowTitle="Lights"></Row> */}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default ControllerDetailCard;
