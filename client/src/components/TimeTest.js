import React from "react";

const TimeTest = () => {
  const [disp, setDisp] = React.useState("Loading...");
  const handleTime = () => {
      let x = new Date()
      let milliDate = '1648334192000'
      let y = new Date(parseInt(milliDate))
    //   setDisp(Math.round(x.getTime() / 1000))
    // setDisp(`${y.getFullYear()}-${y.getMonth()+1}-${y.getDate()} ${y.getHours()}:${y.getMinutes()}:${y.getSeconds()}`)
    // x.setDate(x.getDate()-1)
    setDisp(x.toISOString())

  }
  return (
    <>
      <div onClick={handleTime}>TimeTest</div>
      <div>{disp}</div>
    </>
  );
};

export default TimeTest;
