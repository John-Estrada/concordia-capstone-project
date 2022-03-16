import React from "react";
import PropTypes from "prop-types";
import Button from "./Button";
import axios from "axios";
import { useState, useRef } from "react";
import Ripples from "react-ripples";

const titleStyle = {
  fontSize: 24,
  margin: "8px",
};

const container = {
  width: "256px",
  borderRadius: "8px",
  border: "1px solid black",
  margin: "auto",
  backgroundColor: "white",
  paddingLeft: "32px",
  paddingRight: "32px",
  display: "flex",
  flexDirection: "column",
  gap: "16px",
  paddingBottom: "32px",
};

function AddControllerDialogBox(props) {
  const nameInput = React.useRef(null);
  const [response, setResponse] = React.useState(null);

  const baseUrl = `http://${process.env.REACT_APP_URL}/api/add_controller`;

  const handleConfirm = () => {
    const params = new URLSearchParams();
    params.append("name", nameInput.current.value);
    console.log(nameInput.current.value);
    axios
      .post(baseUrl, params)
      .then((res) => {
        console.log(res);
        if (res.data.result === "failure") {
          setResponse(res.data.message);
        } else {
          props.signalAddController();
          props.handleCancel();
        }
      })
      .catch((err) => {
        console.log(err.reason);
      });
  };
  return (
    <div style={container}>
      <div style={titleStyle}>Add Controller</div>
      <div style={{ display: "flex", flexDirection: "column" }}>
        <div style={{ textAlign: "left", fontSize: "16px" }}>Name</div>
        <input type="text" ref={nameInput}></input>
      </div>
      {response}
      <div style={{ display: "flex", gap: "16px", justifyContent: "flex-end" }}>
        <Ripples color="#fff" during={500}>
          <Button
            text="cancel"
            icon="cancel"
            handleClick={props.handleCancel}
          />
        </Ripples>
        <Ripples color="#fff" during={500}>
          <Button text="confirm" icon="confirm" handleClick={handleConfirm} />
        </Ripples>
      </div>
    </div>
  );
}

export default AddControllerDialogBox;
