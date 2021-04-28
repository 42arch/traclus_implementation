import React from "react"
import { FundFilled } from '@ant-design/icons';
import './AppHeader.css'

class AppHeader extends React.Component {
  render() {
    return (
      <div className="app-header">
        <FundFilled style={{ fontSize: '2.5rem', color: '#fafafa'}} />
        <span id="title">轨迹聚类系统DEMO</span>
      </div>
    )
  }
}

export default AppHeader