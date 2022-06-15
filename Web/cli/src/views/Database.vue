<template>
	<div class="root">
		<div class="nav">
			<navigator />
		</div>
		<div class="box">
			<div class="title"><b>数据表</b></div>
			<div class="right">
				<Dialog />
			</div>
			<el-table :data="table_list" stripe="true">
				<el-table-column label="表名" prop="display_name">
					<template #default="scope">
						<i class="el-icon-document-copy"></i>
						<span style="margin-left: 10px">
							<el-button
								type="text"
								@click="getdata(scope.$index, table_list)"
								>{{ scope.row.display_name }}</el-button
							>
						</span>
					</template>
				</el-table-column>
				<el-table-column label="操作">
					<template #default="scope">
						<el-button
							@click.prevent="deleteRow(scope.$index, table_list)"
							type="text"
							size="small"
						>
							移除
						</el-button>
					</template>
				</el-table-column>
			</el-table>
		</div>
		<div class="databox" v-show="datashow">
			<div class="data">
				<el-descriptions
					class="margin-top"
					title="详细信息"
					:column="2"
					:size="size"
					border
				>
					<el-descriptions-item>
						<template #label>
							<i class="el-icon-s-order"></i>
							表名
						</template>
						{{ display_name }}
					</el-descriptions-item>
					<el-descriptions-item>
						<template #label>
							<i class="el-icon-date"></i>
							源表
						</template>
						{{ table_name }}
					</el-descriptions-item>
					<el-descriptions-item>
						<template #label>
							<i class="el-icon-user"></i>
							所有者
						</template>
						postgresql
					</el-descriptions-item>
					<el-descriptions-item>
						<template #label>
							<i class="el-icon-tickets"></i>
							备注
						</template>
						<el-tag size="small">{{ table_name }}表</el-tag>
					</el-descriptions-item>
					<el-descriptions-item>
						<template #label>
							<i class="el-icon-office-building"></i>
							源数据库
						</template>
						{{ source }}
					</el-descriptions-item>
				</el-descriptions>
				<div class="heads">
					<h3>字段名</h3>
					<el-row >
						<el-col :span="3" v-for="(item, index) in heads" :key="index">
							<el-tag type="success" style="margin-top: 15px;"> {{ item }}</el-tag>
						</el-col>
					</el-row>
				</div>
			</div>
		</div>
	</div>
	<!-- root -->
</template>
<script>
import Navigator from '@/components/Navigator.vue';
import Dialog from '@/components/Dialog.vue';
export default {
	name: 'Database',
	components: {
		Navigator,
		Dialog
	},
	data() {
		return {
			table_list: [],
			tableData: [],
			display_name: '',
			table_name: '',
			source: '',
			datashow: false,
			heads: []
		};
	},
	created() {
		this.$axios.get('/database/tables').then(res => {
			console.log(res.data.table_list);
			this.table_list = res.data.table_list;
		});
	},
	methods: {
		handleDelete(index, row) {
			console.log(index, row);
		},
		deleteRow(index, rows) {
			let data = {
				display_name: rows[index]['display_name'],
				source: rows[index]['source'],
				databaseTablename: rows[index]['table_name']
			};
			this.$axios.post('/database/remove_table', data).then(res => {
				console.log(res.data.code);
			});
			rows.splice(index, 1);
		},
		getdata(index, rows) {
			this.datashow = true;
			console.log(rows[index]); // source     table_name
			this.table_name = rows[index].table_name;
			this.display_name = rows[index].display_name;
			this.source = rows[index].source;
			let data = { uri: rows[index].source, name: rows[index].table_name };
			this.$axios.post('/data/headers', data).then(res => {
				console.log(res.data);
			});
			data = {
				uri: rows[index].source,
				name: rows[index].table_name
			};
			this.$axios.post('/data/headers', data).then(res => {
				this.heads= res.data.column_names;
			});
			
		}
	}
};
</script>
<style lang="less" scoped>
.el-menu-item.is-active {
	border-bottom: none !important;
}
.el-menu--horizontal > .el-menu-item {
	border-bottom: none;
}
.root {
	height: 48.75rem;
	min-height: 100px;
	.box {
		position: relative;
		left: 64.5px;
		top: -789.8px;
		width: 300px;
		height: 789px;
		background-color: white;
		.right {
			position: relative;
			left: 100px;
			top: -12px;
		}
		.title {
			position: relative;
			top: 12px;
			left: -100px;
		}
	}
	.databox {
		position: relative;
		top: -1565px;
		left: 380px;
		background-color: white;
		width: 1140px;
		height: 765px;
		border-radius: 2%;
		box-shadow: 2px 2px 10px #909090;
		border: 2px solid rgba(80, 54, 228, 0.486);
		.data {
			position: relative;
			margin: 10px;
			width: 70rem;
			height: 46.5625rem;
			// background-color: red;
		}
	}
}
.heads {
	h3 {
		position: relative;
		left: -30rem;
	}
	position: relative;
	left: 40px;
	margin-top: 15px;
	border: 1px solid rgba(0, 0, 0, 0.486);
	width: 65rem;
	box-shadow: 1px 1px 2px #505050 inset;
	height: 300px;
}
</style>
