import React from "react";
import "font-awesome/css/font-awesome.min.css";
import { IoMdRefresh, IoAdd } from "react-icons/io";
import {
  BsQuestionCircleFill,
  BsFillCalendarEventFill,
  BsCheckLg,
} from "react-icons/bs";
import { HiOutlinePlus } from "react-icons/hi";
import { BiTime } from "react-icons/bi";
import { FiEdit } from "react-icons/fi";
import { GiCancel } from "react-icons/gi";
import { AiOutlineCheck } from "react-icons/ai";
import { FaCheck, FaFileCsv } from "react-icons/fa";
import styled, { keyframes } from "styled-components";


const iconStyle = {
  fontSize: "18px",
  display: "flex",
  alignItems: "center",
};

const textStyle = {
  fontSize: "18px",
  display: "table-cell",
  alignItems: "center",
  verticalAlign: "sub",
};

function Button(props) {
  let container = {
    backgroundColor: props.disabled ? "#e5e5e5" : "black",
    color: "white",
    gap: "6px",
    padding: "8px",
    display: "inline-flex",
    flexDirection: "row",
    flexBasis: "auto",
    margin: "auto",
    alignItems: "center",
    border: "none",
    borderRadius: "4px",
    cursor: props.disabled ? "default" : "pointer",
    transition: "all 0.4s ease-in",
  };

  let icon = undefined;
  switch (props.icon) {
    case "refresh":
      icon = <IoMdRefresh></IoMdRefresh>;
      break;
    case "add":
      icon = <HiOutlinePlus />;
      break;
    case "calendar":
      icon = <BsFillCalendarEventFill />;
      break;
    case "clock":
      icon = <BiTime />;
      break;
    case "edit":
      icon = <FiEdit />;
      break;
    case "cancel":
      icon = <GiCancel />;
      break;
    case "confirm":
      icon = <FaCheck />;
      break;
    case "csv":
      icon = <FaFileCsv />
      break;
    default:
      icon = <BsQuestionCircleFill></BsQuestionCircleFill>;
      break;
  }

  return (
    <div>
      <button style={container} onClick={props.handleClick}>
        <div style={iconStyle}>{icon}</div>
        <div style={textStyle}>{props.text}</div>
      </button>
    </div>
  );
}

export default Button;
