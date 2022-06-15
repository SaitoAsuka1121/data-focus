<template>
	<!-- 每一个图表 -->
	<div :id="'move' + count" class="panel">
		<div class="chart" :id="'chart' + count"></div>
		<div class="tool">
			<el-button icon="el-icon-error" type="text" @click="del"></el-button>
			<div class="seeview">
				<el-button icon="el-icon-view" type="text"></el-button>
			</div>
			<el-button
				icon="el-icon-setting"
				type="text"
				@click="drawer = true"
			></el-button>
		</div>
		<div class="panel-footer"></div>

		<!-- 一级 -->

		<el-dialog title="添加组件" v-model="Visible" :custom-class="dialogStyle">
			<el-container>
				<el-aside width="200px">
					<el-table :data="table_list">
						<el-table-column label="表名" prop="display_name" width="80px">
							<template #default="scope">
								<i class="el-icon-document-copy"></i>
								<span style="margin-left: 10px">
									<el-button
										type="text"
										@click.prevent="getHeaders(scope.$index, table_list)"
										>{{ scope.row.display_name }}</el-button
									>
								</span>
							</template>
						</el-table-column>
						<el-table-column width="40">
							<template #header>
								<el-button
									icon="el-icon-refresh-right"
									circle
									type="text"
									@click="gettable"
								></el-button>
							</template>
						</el-table-column>
						<el-table-column>
							<template #header>
								<Dialog />
							</template>
						</el-table-column>
					</el-table>
				</el-aside>

				<div class="leftmain">
					<el-table
						:data="column_names"
						empty-text="请选择一张表"
						height="300px"
					>
						<el-table-column label="字段名">
							<template #default="scope">
								<!-- <i class="el-icon-document-copy"></i> -->
								<span style="margin-left: 10px">
									<el-tag type="success">{{ scope.row }}</el-tag>
								</span>
							</template>
						</el-table-column>
					</el-table>
				</div>
			</el-container>
			<div class="button">
				<el-button @click="del" style="width: 170px;">取消</el-button>
				<el-button type="primary" @click="drawer = true" style="width: 170px;"
					>确定</el-button
				>
			</div>
		</el-dialog>
		<!-- 二级 -->
		<el-drawer
			title="我是标题"
			v-model="drawer"
			:with-header="false"
			:show-close="false"
			size="100%"
		>
			<div class="headertool">
				<div class="backbutton">
					<el-button type="text" icon="el-icon-back" @click="drawer = false"
						>返回</el-button
					>
				</div>
				<div class="savechart">
					<el-button
						type="primary"
						icon="el-icon-folder"
						size="small"
						style="width:50px"
						@click="save"
						>保存</el-button
					>
				</div>
			</div>
			<div class="mainbox">
				<div class="cum">
					<el-card>
						<template #header>
							<div class="card-header">
								<div class="leftstr">列单</div>
							</div>
						</template>
						<div class="left">
							<el-table
								:data="column_names"
								empty-text="请选择一张表"
								height="100%"
							>
								<el-table-column label="字段名">
									<template #default="scope">
										<i class="el-icon-document-copy"></i>
										<span style="margin-left: 10px">
											<el-tag type="info" class="cv" effect="plain">{{
												scope.row
											}}</el-tag>
										</span>
									</template>
								</el-table-column>
							</el-table>
						</div>
					</el-card>
				</div>
				<div class="setting">
					<div class="charttype">
						<el-card>
							<div class="charttypebox">
								<div class="button">
									<el-button
										@click="run"
										type="primary"
										v-loading.fullscreen.lock="fullscreenLoading"
										style="width:100px"
										>运行</el-button
									>
								</div>

								<div class="img">
									<div class="line" @click="radio = '折线图'"></div>
									<div class="bar" @click="radio = '柱状图'"></div>
									<div class="pie" @click="radio = '饼图'"></div>
									<div class="scatter" @click="radio = '散点图'"></div>
								</div>
								<!-- <el-radio-group v-model="radio">
									<el-radio-button label="折线图"></el-radio-button>
									<el-radio-button label="柱状图"></el-radio-button>
									<el-radio-button label="散点图"></el-radio-button>
									<el-radio-button label="饼图"></el-radio-button>
									<br />
								</el-radio-group> -->
								<div class="chartsetting">
									<div class="titleinput">
										<h4>标题 :</h4>
										<el-input v-model="chartTitle"></el-input>
									</div>
									<div class="xselect">
										<h4>横轴</h4>
										<el-select
											v-model="x_value"
											filterable
											placeholder="请选择"
										>
											<!-- X的字段选择 -->
											<el-option
												v-for="item in column_names"
												:key="item"
												:label="item"
												:value="item"
											>
											</el-option>
										</el-select>
										<div class="funcx">
											<el-select
												v-model="xdata"
												multiple
												placeholder="请选择"
												:multiple-limit="1"
											>
												<el-option
													v-for="item in options"
													:key="item.value"
													:label="item.label"
													:value="item.value"
												>
												</el-option>
											</el-select>
											<el-radio
												v-model="group_by"
												label="x"
												@change="group_bychange"
												>分组</el-radio
											>
										</div>
										<div class="yselect">
											<h4>竖轴</h4>
											<el-select
												v-model="y_value"
												filterable
												placeholder="请选择"
											>
												<!-- Y的字段选择 -->
												<el-option
													v-for="item in column_names"
													:key="item"
													:label="item"
													:value="item"
												>
												</el-option>
											</el-select>
											<div class="funcy">
												<el-select
													v-model="ydata"
													multiple
													placeholder="请选择"
													:multiple-limit="1"
												>
													<el-option
														v-for="item in options"
														:key="item.value"
														:label="item.label"
														:value="item.value"
													>
													</el-option>
												</el-select>
											</div>
											<div class="gclass">
												<el-radio v-model="group_by" label="y">分组</el-radio>
											</div>
										</div>
									</div>
								</div>
							</div>
						</el-card>
					</div>
				</div>
				<div class="cardleft">
					<el-card>
						<div :id="'view' + count" class="view"></div>
					</el-card>
				</div>
			</div>
		</el-drawer>
	</div>
</template>
<script>
var myChart;
import Dialog from '../components/Dialog.vue';

export default {
	props: ['count'],
	emit: ['closeindex'],
	components: { Dialog },
	data() {
		return {
			Visible: true,
			drawer: false,
			table_list: [],
			column_names: [],
			x_value: '',
			y_value: '',
			chartTitle: '',
			searchtable: '',
			seeting: {},
			getheader: {
				uri: '',
				name: ''
			},
			fullscreenLoading: false,
			xdata: [],
			ydata: [],
			options: [
				{
					value: 'sum(',
					label: '求和'
				},
				{
					value: 'avg(',
					label: '平均'
				},
				{
					value: 'max(',
					label: '最大值'
				},
				{
					value: 'min(',
					label: '最小值'
				},
				{
					value: 'count(',
					label: '计数'
				},
				{
					value: 'count(distinct ',
					label: '唯一计数'
				},
				{
					value: 'stdev(',
					label: '标准差'
				},
				{
					value: 'var(',
					label: '方差'
				}
			],
			xcum: '',
			ycum: '',
			radio: '折线图',
			group_by: 'null',
			charttype: ''
		};
	},
	mounted() {
		// 拖动
		var box = document.getElementById('move' + this.count);
		box.onmousedown = function(event) {
			console.log('chlck');
			var event1 = event;
			var pageX = event1.pageX;
			var pageY = event1.pageY;
			var boxX = pageX - box.offsetLeft;
			var boxY = pageY - box.offsetTop;
			document.onmousemove = function(event) {
				console.log('move');
				var event2 = event;
				var pageX = event2.pageX;
				var pageY = event2.pageY;
				box.style.left = pageX - boxX + 'px';
				box.style.top = pageY - boxY + 'px';
			};
		};
		document.onmouseup = function() {
			document.onmousemove = null;
		};
	},
	methods: {
		// 异步加载
		initEcharts() {
			let newPromise = new Promise(resolve => {
				resolve();
			});
			newPromise.then(() => {
				const echarts = require('echarts/lib/echarts');
				var myChart = echarts.init(
					document.getElementById('chart' + this.count)
				);
				myChart.setOption(this.seeting);
			});
		},
		// 获取字段
		getHeaders(index, rows) {
			console.log(rows);
			let data = {
				uri: rows[index]['source'],
				name: rows[index]['table_name']
			};
			this.$axios.post('/data/headers', data).then(res => {
				this.column_names = res.data.column_names;
			});
			this.getheader = data;
		},
		run() {
			this.fullscreenLoading = true;
			let data;
			if (this.radio == '折线图') {
				this.charttype = 'line';
			} else if (this.radio == '柱状图') {
				this.charttype = 'bar';
			} else if (this.radio == '散点图') {
				this.charttype = 'scatter';
			} else if (this.radio == '饼图') {
				this.charttype = 'pie';
			}
			if (this.group_by == 'x') {
				this.group_by = this.x_value;
				if (this.xdata[0] == undefined && this.ydata[0] == undefined) {
					this.group_by = 'null';
					this.$message({
						message: '分组必须拥有聚集函数',
						type: 'warning'
					});
					this.fullscreenLoading = false;
					return 0;
				}
			} else if (this.group_by == 'y') {
				this.group_by = this.y_value;
				if (this.xdata[0] == undefined && this.ydata[0] == undefined) {
					this.group_by = 'null';
					this.$message({
						message: '分组必须拥有聚集函数',
						type: 'warning'
					});
					this.fullscreenLoading = false;
					return 0;
				}
			} else {
				this.group_by = 'null';
			}

			if (this.xdata[0] != undefined && this.ydata[0] != undefined) {
				data = {
					uri: this.getheader['uri'],
					name: this.getheader['name'],
					columns:
						this.xdata[0] +
						this.x_value +
						'),' +
						this.ydata[0] +
						this.y_value +
						')',
					chartstype: this.charttype,
					group_by: this.group_by
				};
				this.xcum = this.xdata[0] + this.x_value + ')';
				this.ycum = this.ydata[0] + this.y_value + ')';
			} else if (this.xdata[0] == undefined && this.ydata[0] == undefined) {
				data = {
					uri: this.getheader['uri'],
					name: this.getheader['name'],
					columns: this.x_value + ',' + this.y_value,
					chartstype: this.charttype,
					group_by: this.group_by
				};
				this.xcum = this.x_value;
				this.ycum = this.y_value;
			} else if (this.xdata[0] != undefined) {
				data = {
					uri: this.getheader['uri'],
					name: this.getheader['name'],
					columns: this.xdata[0] + this.x_value + '),' + this.y_value,
					chartstype: this.charttype,
					group_by: this.group_by
				};
				this.xcum = this.xdata[0] + this.x_value + ')';
				this.ycum = this.y_value;
			} else {
				data = {
					uri: this.getheader['uri'],
					name: this.getheader['name'],
					columns: this.x_value + ',' + this.ydata[0] + this.y_value + ')',
					chartstype: this.charttype,
					group_by: this.group_by
				};
				this.xcum = this.x_value;
				this.ycum = this.ydata[0] + this.y_value + ')';
			}
			this.$axios.post('/data/query', data).then(res => {
				this.fullscreenLoading = false;

				if (this.radio == '折线图') {
					this.seeting = {
						tooltip: {
							trigger: 'axis'
						},
						title: {
							left: 'center',
							text: this.chartTitle
						},
						toolbox: {
							orient: 'vertical',
							feature: {
								dataZoom: {
									yAxisIndex: 'none'
								},
								restore: {},
								saveAsImage: {}
							}
						},
						xAxis: {
							type: 'category',
							boundaryGap: false,
							data: res.data.result[this.xcum]
						},
						yAxis: {
							type: 'value',
							boundaryGap: [0, '100%']
						},
						dataZoom: [
							{
								type: 'inside',
								start: 0,
								end: 10
							},
							{
								start: 0,
								end: 10
							}
						],
						series: [
							{
								name: '',
								type: 'line',
								symbol: 'none',
								sampling: 'lttb',
								data: res.data.result[this.ycum]
							}
						]
					};
				} else if (this.radio == '柱状图') {
					this.seeting = {
						title: {
							text: this.chartTitle,
							left: 'center'
						},
						toolbox: {
							feature: {
								dataZoom: {
									yAxisIndex: false
								},
								saveAsImage: {
									pixelRatio: 2
								}
							}
						},
						tooltip: {
							trigger: 'axis',
							axisPointer: {
								type: 'shadow'
							}
						},
						grid: {
							bottom: 90
						},
						dataZoom: [
							{
								type: 'inside'
							},
							{
								type: 'slider'
							}
						],
						xAxis: {
							data: res.data.result[this.xcum],
							silent: false,
							splitLine: {
								show: false
							},
							splitArea: {
								show: false
							}
						},
						yAxis: {
							splitArea: {
								show: false
							}
						},
						series: [
							{
								type: 'bar',
								data: res.data.result[this.ycum],
								// Set `large` for large data amount
								large: true
							}
						]
					};
				} else if (this.radio == '散点图') {
					this.seeting = {
						title: {
							text: this.chartTitle,
							left: 'center'
						},
						xAxis: {},
						yAxis: {},
						series: [
							{
								symbolSize: 20,
								data: res.data.result, // [1.2,3.7],
								type: 'scatter'
							}
						]
					};
				} else if (this.radio == '饼图') {
					this.seeting = {
						title: {
							text: this.chartTitle,
							left: 'center'
						},
						tooltip: {
							trigger: 'item'
						},
						legend: {
							top: '5%',
							left: 'center'
						},
						series: [
							{
								name: '数据',
								type: 'pie',
								radius: ['40%', '70%'],
								avoidLabelOverlap: false,
								label: {
									show: false,
									position: 'center'
								},
								emphasis: {
									label: {
										show: true,
										fontSize: '40',
										fontWeight: 'bold'
									}
								},
								labelLine: {
									show: false
								},
								data: res.data.result,
								large: true
							}
						]
					};
				}
				let newPromise = new Promise(resolve => {
					resolve();
				});
				newPromise.then(() => {
					const echarts = require('echarts/lib/echarts');
					if (myChart != null && myChart != '' && myChart != undefined) {
						myChart.dispose(); //销毁
					}
					myChart = echarts.init(document.getElementById('view' + this.count));
					myChart.setOption(this.seeting);
					setTimeout(() => {
						myChart.setOption(this.seeting);
					}, 100);
					console.log(this.seeting);
				});
			});
		},
		save() {
			this.initEcharts();
			this.drawer = false;
			this.Visible = false;
		},
		del() {
			if (this.Visible == true) {
				this.Visible = false;
			}
			this.$emit('func', '');
		},
		log(data) {
			console.log(data);
		},
		gettable() {
			this.$axios.get('/database/tables').then(res => {
				this.table_list = res.data.table_list;
			});
		},
		group_bychange() {
			this.$message({
				message: '分组必须拥有聚集函数',
				type: 'warning'
			});
		}
	},
	created() {
		this.$axios.get('/database/tables').then(res => {
			this.table_list = res.data.table_list;
		});
	}
};
</script>
<style lang="less" scoped>
.panel {
	position: absolute;
	height: 17.7rem;
	left: 4.375rem;
	top: 2.6875rem;
	width: 19.375rem;
	// background: url(../../images/line.png) rgba(255, 255, 255, 0.04);
	&::before {
		position: absolute;
		top: 0;
		left: 0;
		width: 10px;
		height: 10px;
		border-left: 2px solid #02a6b5;
		border-top: 2px solid #02a6b5;
		content: '';
	}

	.panel-footer {
		position: absolute;
		bottom: 0;
		left: 0;
		width: 100%;
		&::before {
			position: absolute;
			left: 0;
			bottom: 0;
			width: 10px;
			height: 10px;
			border-left: 2px solid #02a6b5;
			border-bottom: 2px solid #02a6b5;
			content: '';
		}
	}
	h2 {
		height: 3rem;
		color: black;
		line-height: 3rem;
		text-align: center;
		font-size: 1.25rem;
		font-weight: 400;
	}
	.chart {
		width: 17.7rem;
		height: 17.7rem;
		// background-color: pink;
	}
	.tool {
		height: 17.7rem;
		width: 1.657rem;
		left: 17.7rem;
		position: relative;
		top: -17.7rem;
		// background-color: red;
		&::after {
			position: absolute;
			top: 0;
			right: 0;
			width: 10px;
			height: 10px;
			border-right: 2px solid #02a6b5;
			border-top: 2px solid #02a6b5;
			content: '';
		}
		&::before {
			position: absolute;
			bottom: 0;
			right: 0;
			width: 10px;
			height: 10px;
			border-right: 2px solid #02a6b5;
			border-bottom: 2px solid #02a6b5;
			content: '';
		}
	}
}
* {
	padding: 0;
	margin: 0;
}
.dialogStyle {
	height: 31.25rem;
	width: 50rem;
	border-radius: 2%;
	box-shadow: 2px 2px 10px #000;
}
.button {
	position: relative;
	left: 0;
	top: 0.8rem;
	font-size: 10px;
}
.leftmain {
	position: relative;
	top: 0.375rem;
	left: 0.9375rem;
	max-width: 31.25rem;
	min-width: 6.25rem;
	width: 31.25rem;
	// background-color: #000;
}
.cv {
	text-align: center;
}
.headertool {
	height: 40px;
	border-bottom: 1px solid rgba(0, 0, 0, 0.4);
	// background-color: blue;
	.backbutton {
		position: absolute;
		left: 10px;
	}
	.savechart {
		position: absolute;
		right: 10px;
		top: 5px;
	}
}
.mainbox {
	padding: 0;
	display: flex;
	height: 100%;
	margin: 0 auto;

	.setting {
		position: relative;
		// background-color: cadetblue;
		flex: 0.4;
		.charttype {
			position: absolute;
			height: 3.125rem;
			top: 0.1875rem;
			left: 0.3125rem;
			.charttypebox {
				position: relative;
				width: 20.625rem;
				height: 43.75rem;
				// background-color: red;
				.img {
					position: relative;
					// background-color: red;
					// box-shadow: 2px 2px 10px #909090;
					top: 0.9375rem;
					border: 2px solid rgba(0, 0, 0, 0.2);
					width: 20.625rem;
					height: 15.625rem;
					border-radius: 2%;
					.line {
						width: 3.125rem;
						height: 3.125rem;
						background: url(../../images/type/line.png) no-repeat;
						background-color: white;
						position: relative;
						margin: 0.625rem;
						// background-color: red;
					}
					.line:active {
						border: 2px solid rgba(0, 0, 200, 0.1);
					}
					.bar {
						width: 3.125rem;
						height: 3.125rem;
						background: url(../../images/type/bar.png) no-repeat;
						background-color: white;
						position: relative;
						margin: 10px;
					}
					.bar:active {
						border: 2px solid rgba(0, 0, 200, 0.1);
					}
					.pie {
						width: 3.125rem;
						height: 3.125rem;
						background: url(../../images/type/pie.png) no-repeat;
						background-color: white;
						position: relative;
						margin: 10px;
					}
					.pie:active {
						border: 2px solid rgba(0, 0, 200, 0.1);
					}
					.scatter {
						width: 3.125rem;
						height: 3.125rem;
						background: url(../../images/type/scatter.png) no-repeat;
						background-color: white;
						position: relative;
						margin: 10px;
					}
					.scatter:active {
						border: 2px solid rgba(0, 0, 200, 0.1);
					}
				}
				.button {
					position: relative;
					left: 7.8125rem;
					top: 0.3125rem;
				}
			}
		}
		.chartsetting {
			position: relative;
			position: absolute;
			top: 23rem;
			left: 0rem;
			width: 20.625rem;
			// background-color: pink;
			.titleinput {
				position: relative;
				width: 15rem;
				left: 3rem;
				text-align: left;
				margin-bottom: 15px;
			}
			.xselect {
				position: relative;
				left: 3rem;
				width: 9.375rem;
				h4 {
					text-align: left;
				}
				.yselect {
					position: relative;
					// background-color: red;
					top: -2.8125rem;
					.gclass {
						position: relative;
						top: -2rem;
						left: 7.32rem;
						// background-color:red;
					}
				}
				.funcx {
					position: relative;
					// background-color: red;
					width: 6.25rem;
					top: -2.5rem;
					left: 8.75rem;
				}
				.funcy {
					position: relative;
					// background-color: red;
					width: 6.25rem;
					top: -2.5rem;
					left: 8.75rem;
				}
			}
		}
	}
}
.cardleft {
	position: absolute;
	left: 43.125rem;
	top: 2.6875rem;
}
.view {
	// background-color: red;
	width: 49.375rem;
	min-width: 4.9375rem;
	max-width: 49.375rem;
	height: 43.75rem;
	min-height: 4.375rem;
	max-height: 43.75rem;
}
.left {
	position: relative;
	left: 0.625rem;
	height: 40.3rem;
	max-height: 43.75rem;
	min-height: 4.375rem;
	max-width: 16.625rem;
	min-width: 1.6625rem;
	width: 16.625rem;
	// background-color: red;
}
.cum {
	position: relative;
	top: 0.1875rem;
	.leftstr {
		position: relative;
		text-align: left;
		// background-color: red;
	}
}
/deep/ .updata {
	height: 32.5rem;
	border-radius: 2%;
	box-shadow: 1px 1px 5px black;
}
.select {
	// background-color: red;
	position: relative;
	left: -0rem;
}
.dialog-footer {
	// background-color: red;
	position: relative;
	left: -15rem;
	top: 12rem;
}
</style>
