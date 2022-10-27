import React, { useState, useEffect } from 'react'

function GetItem() {

  const [info, setInfo] = useState([]);  

  useEffect(() => {
    item()
  }, [] )


  const item = async () => {
    fetch(`http://${window.location.host}/api/item/4151`).then((response) => response.json())
    .then((data) => setInfo(data));
  }
 

  {info.map(item => (
          console.log(item)
        ))}

    return(
      <div>
        {
        <li></li>
        }
      </div>
    );
}

export default GetItem