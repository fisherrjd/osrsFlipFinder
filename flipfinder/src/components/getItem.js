import React, { useEffect, useState } from 'react'

function GetItem() {
  const [data, setData] = useState([]);  

  useEffect(() => {
    console.log("here");
    fetch(`http://${window.location.host}/api/item/4151`)
    .then(response => response.json())
    .then(
      data => {
        setData(data);
      }
    );
  }, [] );


    return(
      <div>
        <ul>
       {data.map(item => <li key={data.id}>{data.high}</li>)}
     </ul>
      </div>
    );
}

export default GetItem