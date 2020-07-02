import React, { Component, Fragment } from 'react'
import L from 'leaflet'
import * as esri from 'esri-leaflet'
import {Button, Icon, Input} from 'antd'
import axios from 'axios'
import './Map.css'
import WrappedArgumentsForm from "../components/ArgumentsForm";

import partitionData from '../static/partition_result_test.json'
import clusterData from '../static/clustering_result.json'
import shipData from '../static/ship/aistype_2.json'
import shipClusterData from '../static/ship/ship_data_cluster.json'
import shipRepLineData from '../static/ship/ship_data_rep_line.json'

import {getColorByIndex, getRandomColor} from '../utils'

class Map extends Component {
  constructor() {
    super()
    this.state = {
      data: {}
    }
    this.map = null
    this.overlayer = null
    this.overlayers = []
    this.mapOptions = {maxZoom: 20, minZoom:3, center:[0, 0]}
    // this.getOriginalData = this.getOriginalData.bind(this)
    // this.getClusterData = this.getClusterData.bind(this)
    // this.getReplineData = this.getReplineData.bind(this)
  }
  componentDidMount() {
    this.initMap()
  }

  initMap() {
    this.map = L.map('mapDiv', this.mapOptions).setView([50, 0], 7)
    // 英国位置  [55, 0]  7
    this.addBaseMap()
  }

  getTestApiData() {
    axios.get('http://127.0.0.1:5000/test').then(res => console.log(res.data))
  }

  async addBaseMap() {
    // const base = await esri.tiledMapLayer({
    //   url: 'http://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunity/MapServer'
    // }).addTo(this.map)
    const gray = esri.basemapLayer('DarkGray')
    const street = esri.basemapLayer('Streets').addTo(this.map)
    this.baseLayer = {
      // '基础地图': base,
      '暗色地图': gray,
      '街道地图': street
    }
    L.control.layers(this.baseLayer, this.overLayer).addTo(this.map)
  }

  addJsonLayer() {
    // const style = {'color': 'red', 'weight': 1, 'opacity': 0.8}
    // {color: 'rgb(170, 42.5 , 0)'
    const jsonLayer = L.geoJSON(clusterData, {style: function(feature) { return {color: getColorByIndex(feature.properties.cluster_id)}}})

    jsonLayer.bindPopup(lyr => {
      return `<h3>信息</h3>
        <p>trajectory_id: ${lyr.feature.properties.trajectory_id}</p>
        <p>cluster_id: ${lyr.feature.properties.cluster_id}</p>`
    }).addTo(this.map)

    this.overLayer = {
      '测试数据': jsonLayer
    }
  }
  // getOriginalData(e) {
  //   console.log('获取原始数据')
  //   const style = {'weight': 1, 'opacity': 1}
  //   this.overlayers.forEach(ele => this.map.removeLayer(ele))
  //   const originalDataLayer = L.geoJSON(shipData, style)
  //   originalDataLayer.bindPopup(lyr => {
  //     return `<h3>详细信息</h3>`
  //   }).addTo(this.map)
  //   this.overlayers.push(originalDataLayer)
  // }
  showData = (data) => {
    const style = {'weight': 1, 'opacity': 1}
    this.overlayers.forEach(ele => this.map.removeLayer(ele))
    const originalDataLayer = L.geoJSON(data, style)
    originalDataLayer.bindPopup(lyr => {
      return `<h3>详细信息</h3>
        <p>shipInfo：</p>`
    }).addTo(this.map)
    this.overlayers.push(originalDataLayer)
  }

  showPartitionData = (data) => {
    console.log('显示分段数据')
    const style = {}
    this.overlayers.forEach(ele => this.map.removeLayer(ele))
    const partitionDataLayer = L.geoJSON(data, {style: function(feature) { return { 
      color: getColorByIndex(feature.properties.trajectory_id),
      'weight': 1, 'opacity': 1
    }}})
    partitionDataLayer.bindPopup(lyr => {
      return `<h3>详细信息</h3>
        <p>trajectory_id: ${lyr.feature.properties.trajectory_id}</p>`
    }).addTo(this.map)
    this.overlayers.push(partitionDataLayer)
  }

  // getClusterData(e) {
  //   console.log('显示聚类结果数据')
  //   const style = {'weight': 1, 'opacity': 0.8}
  //   this.overlayers.forEach(ele => this.map.removeLayer(ele))
  //   const clusterDataLayer = L.geoJSON(shipClusterData, {style: function(feature) { return {
  //     color: getColorByIndex(feature.properties.cluster_id),
  //     'weight': 1, 'opacity': 1
  //   }}})
  //   clusterDataLayer.bindPopup(lyr => {
  //     return `<h3>详细信息</h3>
  //       <p>trajectory_id: ${lyr.feature.properties.trajectory_id}</p>
  //       <p>cluster_id: ${lyr.feature.properties.cluster_id}</p>`
  //   }).addTo(this.map)
  //   this.overlayers.push(clusterDataLayer)
  // }

  showClustersData = (data) => {
    console.log('显示聚类数据')
    const style = {'weight': 1, 'opacity': 0.8}
    this.overlayers.forEach(ele => this.map.removeLayer(ele))
    const clusterDataLayer = L.geoJSON(data, {style: function(feature) { return {
      color: getColorByIndex(feature.properties.cluster_id),
      'weight': 1, 'opacity': 1
    }}})
    clusterDataLayer.bindPopup(lyr => {
      return `<h3>详细信息</h3>
        <p>trajectory_id: ${lyr.feature.properties.trajectory_id}</p>
        <p>cluster_id: ${lyr.feature.properties.cluster_id}</p>`
    }).addTo(this.map)
    this.overlayers.push(clusterDataLayer)
  }

  // getReplineData(e) {
  //   console.log('显示代表性轨迹数据')
  //   const style = {'color': 'yellow', 'weight': 2, 'opacity': 1}
  //   // this.overlayers.forEach(ele => this.map.removeLayer(ele))
  //   const replineDataLayer = L.geoJSON(shipRepLineData, style)
  //   replineDataLayer.bindPopup(lyr => {
  //     return `<h3>详细信息</h3>`
  //   }).addTo(this.map)
  //   this.overlayers.push(replineDataLayer)
  // }

  showReplinesData = (data) => {
    const style = {'color': 'yellow', 'weight': 2, 'opacity': 1}
    const replineDataLayer = L.geoJSON(data, style)
    replineDataLayer.bindPopup(lyr => {
      return `<h3>详细信息</h3>`
    }).addTo(this.map)
    this.overlayers.push(replineDataLayer)
  }

  render() {
    return (
      <Fragment>
        <div className="map" id="map">
          <div className="mapDiv" id="mapDiv"></div>
          <div className="handleDiv" id="handleDiv">
            <h3>轨迹聚类计算</h3>
            <WrappedArgumentsForm ref="argumentDiv" 
              ShowData={this.showData}
              ShowPartitionData={this.showPartitionData}
              ShowClustersData={this.showClustersData}
              ShowReplinesData={this.showReplinesData}>  
            </WrappedArgumentsForm>
          </div>
        </div>
      </Fragment>
    )
  }
}


export default Map