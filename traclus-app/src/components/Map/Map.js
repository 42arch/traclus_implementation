import React from "react"
import './Map.css'
import L from 'leaflet'
import * as esri from 'esri-leaflet'
import emitter from "../../utils/event";
import { getColorByIndex } from "../../utils/color";

class Map extends React.Component {
  constructor() {
    super()
    this.state = {

    }
    this.map = Object.create(null)
    this.opLayers = []
    this.mapOptions = {maxZoom: 20, minZoom:3, center:[0, 0]}
  }

  componentDidMount() {
    this.initMap()
    this.eventEmitter = emitter.addListener('createLayer', data => {
      this.createGeoJsonLayer(data)
    })

    this.showPartitionEvent = emitter.addListener('showPartition', data => {
      this.showPartitionData(data)
    })

    this.showCLusterEvent = emitter.addListener('showCluster', data => {
      this.showClusterData(data)
    })

    this.showRepLineEvent = emitter.addListener('showRepLine', data => {
      this.showRepLineData(data)
    })

    this.eventEmitter2 = emitter.addListener('removeLayer', () => {
      this.removeOpLayers()
    })
  }

  initMap() {
    console.log('L', L)
    this.map = L.map("map", this.mapOptions).setView([30, 120], 6)
    this.addBaseMap()
  }

  async addBaseMap() {
    let base = await esri.tiledMapLayer({
      url: 'http://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunity/MapServer'
    }).addTo(this.map)

    let darkBlue = await esri.tiledMapLayer({
      url: 'http://map.geoq.cn/arcgis/rest/services/ChinaOnlineStreetPurplishBlue/MapServer'      
    })

    let grey = await esri.tiledMapLayer({
      url: 'http://map.geoq.cn/arcgis/rest/services/ChinaOnlineStreetGray/MapServer'
    })

    let ocean = await esri.tiledMapLayer({
      url: 'http://server.arcgisonline.com/arcgis/rest/services/Ocean/World_Ocean_Base/MapServer'
    })
    let street = esri.basemapLayer('Streets')

    this.baseLayer = {
      '基础地图': base,
      '海洋地形': ocean,
      '暗色地图': darkBlue,
      '灰色地图': grey,
      '街道地图': street
    }
    L.control.layers(this.baseLayer, this.overLayer).setPosition('topleft').addTo(this.map)
  }

  createGeoJsonLayer(data) {
    this.removeOpLayers()
    console.log('create layer!', data)
    let opLayer = L.geoJSON(data, {
      style: function(feature) {
        return {color: '#096dd9', weight: 1, opacity: 0.8 }
      }
    }).addTo(this.map)

    this.map.fitBounds(opLayer.getBounds())
    this.opLayers.push(opLayer)
  }

  showPartitionData(data) {
    this.removeOpLayers()
    let partitionLayer = L.geoJSON(data, {style: function(feature) { return { 
      color: getColorByIndex(feature.properties.trajectory_id),
      'weight': 1, 'opacity': 1
    }}})
    partitionLayer.bindPopup(lyr => {
      return `<h3>详细信息</h3>
        <p>trajectory_id: ${lyr.feature.properties.trajectory_id}</p>`
    }).addTo(this.map)
    this.opLayers.push(partitionLayer)
  }

  showClusterData(data) {
    console.log('显示cluster')
    this.removeOpLayers()
    let clusteLayer = L.geoJSON(data, {style: function(feature) { return {
      color: getColorByIndex(feature.properties.cluster_id),
      'weight': 1, 'opacity': 1
    }}})
    clusteLayer.bindPopup(lyr => {
      return `<h3>详细信息</h3>
        <p>trajectory_id: ${lyr.feature.properties.trajectory_id}</p>
        <p>cluster_id: ${lyr.feature.properties.cluster_id}</p>`
    }).addTo(this.map)
    this.opLayers.push(clusteLayer)
  }

  showRepLineData(data) {
    let style = {'color': 'yellow', 'weight': 2, 'opacity': 1}
    let repLineLayer = L.geoJSON(data, style)
    repLineLayer.bindPopup(lyr => {
      return `<h3>详细信息</h3>`
    }).addTo(this.map)
    this.opLayers.push(repLineLayer)
  }

  removeOpLayers() {
    this.opLayers.forEach(lyr => this.map.removeLayer(lyr))
  }



  render() {
    return (
      <div className="app-map" id="map">
      </div>
    )
  }
}

export default Map