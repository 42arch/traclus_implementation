import { Form, Input, Button, InputNumber, Collapse, Spin, message, Tooltip } from 'antd';
import React, { Fragment } from 'react'
import axios from 'axios'

function hasErrors(fieldsError) {
  return Object.keys(fieldsError).some(field => fieldsError[field]);
}

const { TextArea } = Input
const { Panel } = Collapse

class ArgumentsForm extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      values: {},
      loading: false
    }

    this.showOriginData = this.showOriginData.bind(this)
  }

  componentDidMount() {
    // To disable submit button at the beginning.
    this.props.form.validateFields();
  }

  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        this.setState({
          values: values
        })
      }
    })
    console.log(this.state.values)
  }

  showOriginData(e) {
    this.setState({loading: true})
    console.log('显示原始数据')
    const {getFieldValue} = this.props.form
    const data = getFieldValue('data')
    if (typeof(data) != "undefined") {
      const dataObj = JSON.parse(data)
      this.props.ShowData(dataObj)
    } else {
      message.warning("请先输入原始数据！")
    }

    this.setState({loading: false})
  }
  showPartitionRes = () => {
    this.setState({loading: true})
    let jsonData = this.state.values.data
    // let epsilon = this.state.values.epsilon
    let data = new FormData()
    data.append('data', jsonData)
    // data.append('epsilon', 11111)
    console.log(data)
    axios.defaults.headers.post['Content-Type'] = 'application/json'
    axios.post('http://127.0.0.1:5000/api/partitions/', data, {headers: {'Access-Control-Allow-Origin': '*'}}).then(
      res => {
        let partitionResObj = JSON.parse(res.data)
        console.log(partitionResObj)
        this.props.ShowPartitionData(partitionResObj)
        this.setState({loading: false})
      }
    )
  }
  showClusters = () => {
    console.log('显示聚类结果')
    this.setState({loading: true})
    let jsonData = this.state.values.data
    let epsilon = this.state.values.epsilon
    let min_neighbors = this.state.values.min_neighbors
    let data = new FormData()
    data.append('data', jsonData)
    data.append('epsilon', epsilon)
    data.append('min_neighbors', min_neighbors)
    axios.post('http://127.0.0.1:5000/api/clusters/', data).then(
      res => {
        let clustersObj = JSON.parse(res.data)
        console.log(clustersObj)
        this.props.ShowClustersData(clustersObj)
        this.setState({loading: false})
      }
    )
  }

  showRepLines = () => {
    console.log("显示代表性轨迹")
    this.setState({loading:true})
    let jsonData = this.state.values.data
    let epsilon = this.state.values.epsilon
    let min_neighbors = this.state.values.min_neighbors
    let min_num_trajs = this.state.values.min_num_trajectories
    let min_vertical_lines = this.state.values.min_vertical_lines
    let min_prev_dist = this.state.values.min_prev_dist
    let data = new FormData()
    data.append('data', jsonData)
    data.append('epsilon', epsilon)
    data.append('min_neighbors', min_neighbors)
    data.append('min_num_trajectories_in_cluster', min_num_trajs)
    data.append('min_vertical_lines', min_vertical_lines)
    data.append('min_prev_dist', min_prev_dist)
    axios.post('http://127.0.0.1:5000/api/rep_lines/', data).then(
      res => {
        let replinesObj = JSON.parse(res.data)
        console.log(replinesObj)
        this.props.ShowReplinesData(replinesObj)
        this.setState({loading: false})
      }
    )
  }


  render() {
    const { getFieldDecorator, getFieldsError, getFieldError, isFieldTouched } = this.props.form;

    // Only show error after a field is touched.
    const dataError = isFieldTouched('data') && getFieldError('data')
    const epsilonError = isFieldTouched('epsilon') && getFieldError('epsilon')
    const minNeighborsError = isFieldTouched('min_neighbors') && getFieldError('min_neighbors')
    const minNumTrajError = isFieldTouched('min_num_trajectories') && getFieldError('min_num_trajectories')
    const minVertLinesError = isFieldTouched('min_vertical_lines') && getFieldError('min_vertical_lines')
    const minPrevDistError = isFieldTouched('min_prev_dist') && getFieldError('min_prev_dist')

    return (
        <Form onSubmit={this.handleSubmit}>
          <Collapse defaultActiveKey={['2']}>
            <Panel header="输入原始数据" id="dataPanel">
              <Form.Item validateStatus={dataError ? 'error' : ''} help={dataError || ''}>
                {getFieldDecorator('data', {
                  rules: [{ required: true, message: '请输入Geojson数据!' }],
                })(
                  <TextArea rows={5} allowClear/>
                )}
              </Form.Item>
            </Panel>
            <Panel header="输入算法参数" id='argumentsPanel'>
              <Form.Item validateStatus={epsilonError ? 'error' : ''} help={epsilonError || ''}>
                <Tooltip placement="bottomLeft" title="epsilon参数">
                epsilon:
                </Tooltip>
              
                {getFieldDecorator('epsilon', {
                  rules: [{ required: true, message: '请输入参数epsilon!' }],
                })(
                  <InputNumber placeholder="epsilon" step={0.01}/>,
                )}
              </Form.Item>
              <Form.Item validateStatus={minNeighborsError ? 'error' : ''} help={minNeighborsError || ''}>
                min_neighbors:
                {getFieldDecorator('min_neighbors', {
                  rules: [{ required: true, message: '请输入参数min_neighbors!' }],
                })(
                  <InputNumber placeholder="min_neighbors" />,
                )}
              </Form.Item>
              <Form.Item validateStatus={minNumTrajError ? 'error' : ''} help={minNumTrajError || ''}>
                min_num_trajectories_in_cluster:
                {getFieldDecorator('min_num_trajectories', {
                  rules: [{ required: true, message: '请输入参数min_num_trajectories!' }],
                })(
                  <InputNumber placeholder="min_num_trajectories_in_cluster"/>,
                )}
              </Form.Item>
              <Form.Item validateStatus={minVertLinesError ? 'error' : ''} help={minVertLinesError || ''}>
                min_vertical_lines:
                {getFieldDecorator('min_vertical_lines', {
                  rules: [{ required: true, message: '请输入参数min_vertical_lines!' }],
                })(
                  <InputNumber placeholder="min_vertical_lines"/>,
                )}
              </Form.Item>
              <Form.Item validateStatus={minPrevDistError ? 'error' : ''} help={minPrevDistError || ''}>
                min_prev_dist:
                {getFieldDecorator('min_prev_dist', {
                  rules: [{ required: true, message: 'min_prev_dist!' }],
                })(
                  <InputNumber placeholder="min_prev_dist" step={0.01}/>,
                )}
              </Form.Item>
              
              <Button id="confirmButton" type="primary" htmlType="submit" disabled={hasErrors(getFieldsError())}>
                确认
              </Button>
            </Panel>
            <Panel showArrow={false} header="       计算与显示">
            <Form.Item>
              <Spin spinning={this.state.loading} tip="加载数据中" id="handleContainer">
                <Button id="handleButton" shape="round" type="primary" size="default"
                  onClick={this.showOriginData}>显示原始数据</Button>
                <Button id="handleButton" shape="round" type="primary" size="default"
                  onClick={this.showPartitionRes}>获取显示分段结果</Button>
                <Button id="handleButton" shape="round" type="primary" size="default"
                  onClick={this.showClusters}>获取显示聚类结果</Button>
                <Button id="handleButton" shape="round" type="primary" size="default"
                  onClick={this.showRepLines}>获取显示代表性轨迹</Button>
              </Spin>

            </Form.Item>
            </Panel>

          </Collapse>
        </Form>
    );
  }
}

const WrappedArgumentsForm = Form.create({ name: 'horizontal_login' })(ArgumentsForm);
export default WrappedArgumentsForm

// ReactDOM.render(<WrappedHorizontalLoginForm />, mountNode);