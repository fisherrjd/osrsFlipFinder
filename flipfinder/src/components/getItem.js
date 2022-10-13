import React, { useEffect, useState } from 'react'

function GetItem() {
  const [data, setData] = useState(null);  

  useEffect(() => {
    console.log("here");
    fetch("http://localhost:8000/item/4151")
    .then(response => response.json())
    .then(
      data => {
        setData(data);
      }
    );
  }, [] );


    return(
      <div>test</div>
    );
}

export default GetItem