import React from "react";
import styled, { keyframes, css } from "styled-components";

const flash = keyframes`
  from {
      width: 10px;
      height: 10px;
      display: inline;
    }

  to {
    display: inline;
    width: 100px;
    height: 100px;
  }
`;

const StyledTile = styled.div`
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: pink;
  position: absolute;
  left: ${(props) => props.x};
  top: ${(props) => props.y};
  display: ${(props) => (props.display ? "none" : "inline-block")}
  animation: ${(props) =>
    css`
      ${flash} 0.1s linear 3
    `};
`;

const TestComponent = () => {
  const st = React.useRef(null);

  const handleClick = (e) => {
    setX(e.clientX - 50 + "px");
    setY(e.clientY - 50 + "px");
    setDisplay(true);
    setDoAnimate(true);
    setTimeout(() => {
      console.log("timeout");
      setDisplay(false);
    }, 400);
  };

  const [doAnimate, setDoAnimate] = React.useState(false);
  const [x, setX] = React.useState("0px");
  const [y, setY] = React.useState("0px");
  const [display, setDisplay] = React.useState(false);

  return (
    <div ref={st}>
      {display ? (
        <StyledTile animate={doAnimate} x={x} y={y} display={display} />
      ) : null}
      <button onClick={handleClick} style={{ width: "100px", height: "100px" }}>
        Animate
      </button>
      <StyledTile></StyledTile>
    </div>
  );
};

export default TestComponent;
