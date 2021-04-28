function getColorByIndex(i){
  if(i<10)i=i*302.3;
  if(i<100)i=i*31.2;
  for(;i>255;i*=0.98);
  var temp=i.toString().substring(i.toString().length-3);
  i+=parseInt(temp);
  for(;i>255;i-=255);
  i=parseInt(i);
  if(i<10)i+=10;

  var R=i*(i/100);
  for(;R>255;R-=255);
  if(R<50)R+=60;
  R=parseInt(R).toString(16);

  var G=i*(i%100);
  for(;G>255;G-=255);
  if(G<50)G+=60;
  G=parseInt(G).toString(16);

  var B=i*(i%10);
  for(;B>255;B-=255);
  if(B<50)B+=60;
  B=parseInt(B).toString(16);

  return "#"+R+G+B;
}


function getRandomColor() {
  const rgb = []
  for (let i = 0 ; i < 3; ++i){
    let color = Math.floor(Math.random() * 256).toString(16)
    color = color.length === 1 ? '0' + color : color
    rgb.push(color)
  }
  return '#' + rgb.join('')
}

export {getColorByIndex, getRandomColor}