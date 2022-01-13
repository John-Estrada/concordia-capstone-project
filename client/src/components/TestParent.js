import React from "react";
import Button from "./Button";
import styled from "styled-components";
import Ripples from "react-ripples";

const Inner = styled.div`
  height: 100px;
  width: 100px;
  text-align: center;
  background: white;
`;

const TestParent = () => {
  return (
    <div>
      <Ripples color="#fff" during={500}>
        <Button></Button>
      </Ripples>
    </div>
  );
};

export default TestParent;
