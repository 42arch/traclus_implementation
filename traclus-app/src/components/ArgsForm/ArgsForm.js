import React from "react"
import axios from "axios"
import { Form, Collapse, Upload, message, Button, Spin, InputNumber } from "antd"
import { UploadOutlined } from '@ant-design/icons'
import emitter from "../../utils/event";
import './ArgsForm.css'

const { Panel } = Collapse

const layout = {
  labelCol: {
    span: 6,
  },
  wrapperCol: {
    span: 18,
  },
}

const tailLayout = {
  wrapperCol: {
    offset: 8,
    span: 16,
  },
}

const uploadProps = {
  name: 'file',
  accept: '.json',
  headers: {
    authorization: 'authorization-text',
  }
}


const validateMessages = {
  required: '${label} is required!',
  types: {
    email: '${label} is not a valid email!',
    number: '${label} is not a valid number!',
  },
  number: {
    range: '${label} must be between ${min} and ${max}',
  },
}

class ArgsForm extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      values: {},
      algorithmParams: {},
      uploadStatus: '',
      originData: null,
      loading: false
    }
    this.customRequest = this.customRequest.bind(this)
    this.onChange = this.onChange.bind(this)
    this.onFinish = this.onFinish.bind(this)
    this.isParamsNull = this.isParamsNull.bind(this)
    this.getPartitions = this.getPartitions.bind(this)
    this.getClusters = this.getClusters.bind(this)
    this.getRepLines = this.getRepLines.bind(this)
  }

  componentDidMount() {
    
  }

  componentWillUnmount() {

  }

  customRequest(info) {
    let config = {
      headers: { "Content-Type": "multipart/form-data" }
    }
    let param = new FormData()
    param.append('file', info.file)
    axios.post('http://127.0.0.1:5000/api/file', param, config).then(res => {
      if(res.status === 201) {
        try {
          let geoData = JSON.parse(res.data.content)
          this.setState({originData: geoData})
          this.setState({uploadStatus: 'done'})
          emitter.emit('createLayer', geoData)
          message.success('GeoJSON文件上传并解析成功!')
        } catch (error) {
          this.setState({uploadStatus: 'error'})
          message.error('根据GeoJSON创建图层失败，请移除并检查数据!')
        }
      } else {
        this.setState({uploadStatus: 'error'})
      }
    })
  }

  onChange(e) {
    console.log(233, e)
    e.file.status = this.state.uploadStatus
  }
  onRemove(e) {
    emitter.emit('removeLayer')
  }

  onFinish(v) {
    console.log('Success:', v)
    message.success('参数提交成功!')
    // this.state.algorithmParams = v
    this.setState({algorithmParams: v})
  }

  onFinishFailed(errorInfo){
    console.log('Failed:', errorInfo);
  }

  isParamsNull() {
    if(!!this.state.originData && !!this.state.algorithmParams) {
      let alParams = this.state.algorithmParams
      if(alParams.epsilon && alParams.min_neighbors && alParams.min_num_trajs_in_cluster && alParams.min_prev_dist && alParams.min_vertical_lines) {
        return true
      }
    } else {
      message.warn('确认上传原始数据和参数')
      return false
    }
  }

  // 获取轨迹分段
  getPartitions() {
    this.setState({loading: true})
    let flag = this.isParamsNull()
    if(flag) {
      let params = new FormData()
      params.append('data', JSON.stringify(this.state.originData))
      axios.post('http://127.0.0.1:5000/api/partitions', params).then(res => {
        // console.log('part', res.data)
        emitter.emit('showPartition', JSON.parse(res.data))
        this.setState({loading: false})
      })
    }
  }

  // 获取轨迹聚类
  getClusters() {
    this.setState({loading: true})
    let flag = this.isParamsNull()
    if(flag) {
      let params = new FormData()
      params.append('data', JSON.stringify(this.state.originData))
      params.append('epsilon', this.state.algorithmParams.epsilon)
      params.append('min_neighbors', this.state.algorithmParams.min_neighbors)
      axios.post('http://127.0.0.1:5000/api/clusters', params).then(res => {
        // console.log('cluster', res.data)
        emitter.emit('showCluster', JSON.parse(res.data))
        this.setState({loading: false})
      })
    }
  }

  // 获取代表轨迹
  getRepLines() {
    this.setState({loading: true})
    let flag = this.isParamsNull()
    if(flag) {
      let params = new FormData()
      params.append('data', JSON.stringify(this.state.originData))
      params.append('epsilon', this.state.algorithmParams.epsilon)
      params.append('min_neighbors', this.state.algorithmParams.min_neighbors)
      params.append('min_num_trajectories_in_cluster', this.state.algorithmParams.min_num_trajs_in_cluster)
      params.append('min_vertical_lines', this.state.algorithmParams.min_vertical_lines)
      params.append('min_prev_dist', this.state.algorithmParams.min_prev_dist)
      axios.post('http://127.0.0.1:5000/api/rep_lines', params).then(res => {
        console.log(res.data)

        emitter.emit('showRepLine', JSON.parse(res.data))
        this.setState({loading: false})
      })
      
    }
  }


  render() {
    return (
      <div className="app-form">
        <span id="title">轨迹聚类计算</span>
        <Collapse className="form-panel">
          <Panel header="上传原始数据" key="1">
            <Upload {...uploadProps} customRequest={this.customRequest} onChange={this.onChange} onRemove={this.onRemove}>
              <Button icon={<UploadOutlined />}>上传GeoJSON数据</Button>
            </Upload>
          </Panel>
          <Panel header="提交算法参数" key="2">
            <Form {...layout} onFinish={this.onFinish} onFinishFailed={this.onFinishFailed} validateMessages={validateMessages}>
              <Form.Item label="eps" name="epsilon" className="form-item" initialValue={0.06} rules={[{ required: true, message: '需要eps参数!' }]}>
                <InputNumber size="small" placeholder="epsilon" step={0.01}/>
              </Form.Item>
              <Form.Item label="min_n" name="min_neighbors" className="form-item" initialValue={8} rules={[{ required: true, message: '需要min_neighbors参数!' }]}>
                <InputNumber size="small" placeholder="min_neighbors" step={1}/>
              </Form.Item>
              <Form.Item label="min_trajs" name="min_num_trajs_in_cluster" className="form-item" initialValue={12} rules={[{ required: true, message: '需要min_num_trajs_in_cluster参数!' }]}>
                <InputNumber size="small" placeholder="min_num_trajectories_in_cluster" step={1}/>
              </Form.Item>
              <Form.Item label="min_vl" name="min_vertical_lines" className="form-item" initialValue={4} rules={[{ required: true, message: '需要min_vertical_lines参数!' }]}>
                <InputNumber size="small" placeholder="min_vertical_lines" step={1}/>
              </Form.Item>
              <Form.Item label="min_pd" name="min_prev_dist" className="form-item" initialValue={0.01} rules={[{ required: true, message: '需要min_prev_dist参数!' }]}>
                <InputNumber size="small" placeholder="min_prev_dist" step={0.01}/>
              </Form.Item>
              <Form.Item {...tailLayout}>
                <Button size="small" id="confirmButton" type="primary" htmlType="submit">
                  提交参数
                </Button>
              </Form.Item>
            </Form>
          </Panel>
          <Panel header="计算与显示" key="3">

          <Spin spinning={this.state.loading}> 
            <div className="calcButtons">
              <Button size="small" id="confirmButton" onClick={this.getPartitions} type="default">
                轨迹分段
              </Button>
              <Button size="small" id="confirmButton" onClick={this.getClusters} type="default">
                轨迹聚类
              </Button>
              <Button size="small" id="confirmButton" onClick={this.getRepLines} type="default">
                代表性轨迹
              </Button>
            </div>
          </Spin>


          </Panel>
        </Collapse>
      </div>
    )
  }
}

export default ArgsForm