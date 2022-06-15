<template>
	<div class="chart"></div>
</template>

<script>
export default {
	data() {
		return {};
	},
	computed: {},
	mounted() {
		const echarts = require('echarts/lib/echarts');
		var myChart = echarts.init(document.getElementById('.chart'));
		myChart.setOption({
			title: {
				text: 'ECharts 入门示例'
			},
			tooltip: {},
			xAxis: {
				data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
			},
			yAxis: {},
			series: [
				{
					name: '销量',
					type: 'bar',
					data: [5, 20, 36, 10, 10, 20]
				}
			]
		});
	},
	methods: {
	
	}
};
</script>
<style scoped>
.chart {
	width: 25rem;
	height: 25rem;
}
</style>
