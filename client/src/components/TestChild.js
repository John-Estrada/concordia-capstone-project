import React from "react";
import styled, { keyframes, css } from "styled-components";

const Heading = keyframes`
  0% { width: 10px; height: 10px; transform: translateY(0px) translateX(0px);  }
  100% { width: 200px; height: 200px; transform:translateY(-100px) translateX(-100px)}
`;

const Outer = styled.div`
  display: block;
  flex-direction: column;
  align-items: center;
  font-size: 1.5em;
  border: 1px solid black;
  overflow: hidden;
`;

const Inner = styled.div`
  background-color: white;
  opacity: 50%;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  h1 {
    font-weight: lighter;
  }
  position: absolute;
  top: ${(props) => props.y};
  left: ${(props) => props.x};
  animation: ${Heading};
  animation-duration: 250ms;
  animation-fill-mode: forwards;
  display: block;
`;

const TestChild = () => {
  const [shown, setShown] = React.useState(false);
  const [x, setX] = React.useState("0px");
  const [y, setY] = React.useState("0px");

  const handleClick = (e) => {
    console.log(e.clientX);
    setY(e.pageY + "px");
    setX(e.pageX + "px");
    console.log(y);
    setShown(true);
    setTimeout(() => {
      setShown(false);
    }, 250);
  };

  return (
    <Outer onClick={handleClick}>
      {shown ? <Inner y={y} x={x}></Inner> : null}
      <button>Click here</button>
    </Outer>
  );
};

export default TestChild;
