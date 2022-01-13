import React from "react";

let selected = false;

function ControllerThumbnailCard(props) {
  props.selected === "true" ? (selected = true) : (selected = false);

  const container = {
    border: "1px solid black",
    borderRadius: "8px",
    display: "flex",
    gap: "20px",
    padding: "0.75em",
    backgroundColor: selected ? "black" : "white",
    color: selected ? "white" : "black",
    cursor: "pointer",
  };

  return (
    <div style={container} onClick={props.handleClick}>
      <div>{props.id}</div>
      <div>{props.name}</div>
    </div>
  );
}

export default ControllerThumbnailCard;
