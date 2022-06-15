<template>
	<div class="root">
		<div class="nav">
			<navigator />
		</div>
		<div class="box">
			<div class="title"><b>数据库</b></div>
			<div class="right">
				<el-button
					type="primary"
					@click="dialogFormVisible = true"
					size="mini"
					style="float:right"
					>添加连接</el-button
				>
			</div>
			<el-table :data="DataList" stripe ="true">
				<el-table-column label="数据库名" prop="display_name">
					<template #default="scope">
						<i class="el-icon-coin"></i>
						<span style="margin-left: 10px">
							<el-button type="text" @click="getdata(scope.$index, DataList)">{{
								scope.row.display_name
							}}</el-button>
						</span>
					</template>
				</el-table-column>
				<el-table-column label="操作">
					<template #default="scope">
						<el-button
							@click.prevent="deleteRow(scope.$index, DataList)"
							type="text"
							size="small"
						>
							移除
						</el-button>
					</template>
				</el-table-column>
			</el-table>
		</div>
		<div class="databox" v-show="databoxshow">
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
							库名
						</template>
						{{display_name}}
					</el-descriptions-item>
					<el-descriptions-item>
						<template #label>
							<i class="el-icon-date"></i>
							源库名
						</template>
						{{display_name}}
					</el-descriptions-item>
					<el-descriptions-item>
						<template #label>
							<i class="el-icon-user"></i>
							所有者
						</template>
						{{owner}}
					</el-descriptions-item>
					<el-descriptions-item>
						<template #label>
							<i class="el-icon-tickets"></i>
							备注
						</template>
						<el-tag size="small">{{display_name}}表</el-tag>
					</el-descriptions-item>
					<el-descriptions-item>
						<template #label>
							<i class="el-icon-office-building"></i>
							数据库URI
						</template>
						{{sqlalchemy_uri}}
					</el-descriptions-item>
				</el-descriptions>
				<div class="heads">
					<h3>表名</h3>
					<el-row >
						<el-col :span="3" v-for="(item, index) in table_list" :key="index">
							<el-tag type="success" style="margin-top: 15px;"> {{ item.display_name }}</el-tag>
						</el-col>
					</el-row>
				</div>
			</div>
		</div>
		<div class="dialog">
			<el-dialog
				title="数据选择"
				v-model="dialogFormVisible"
				custom-class="size"
				width="40%"
			>
				<div class="formsize">
					<el-form ref="form" :model="form">
						<el-form-item label="数据库名">
							<el-input v-model="form.display_name"></el-input>
						</el-form-item>
						<el-form-item label="数据库URI">
							<el-input
								v-model="form.sqlalchemy_uri"
								placeholder="postgresql://username:password@hostname:port/database"
							></el-input>
						</el-form-item>
					</el-form>
					<div class="accbutton">
						<el-button type="primary" @click="testlink('form')"
						>测试链接</el-button
					>
					<el-button @click="postlink('form')">保存</el-button>
					<el-button type="success" @click="dialogFormVisible = false">取消</el-button>
					</div>
				</div>
			</el-dialog>
		</div>
	</div>
</template>
<script>
import Navigator from '../components/Navigator.vue';
export default {
	name: 'Home',
	components: { Navigator },
	data() {
		return {
			DataList: [],
			dialogFormVisible: false,
			form: {
				display_name: '',
				sqlalchemy_uri: 'postgresql://username:password@hostname:port/database'
			},
			display_name: '',
			owner: '',
			sqlalchemy_uri: '',
			databoxshow:false,
			table_list:[],
		};
	},
	created() {
		this.$axios.get('database/list').then(res => {
			this.DataList = res.data.database_list;
			console.log(this.DataList);
		});
	},
	methods: {
		testlink(form) {
			this.$refs[form].validate(valid => {
				if (valid) {
					let { sqlalchemy_uri } = this.form;
					let data = {
						sqlalchemy_uri: sqlalchemy_uri
					};
					this.$axios.post('/database/test', data).then(res => {
						console.log(res);
						if (res.data.code == 0) {
							this.$message({
								message: '链接可用',
								type: 'success'
							});
						} else {
							this.$message({
								message: res.data.message,
								type: 'error'
							});
						}
					});
				}
			});
		},
		postlink(form) {
			this.$refs[form].validate(valid => {
				if (valid) {
					let { sqlalchemy_uri } = this.form;
					let data = {
						sqlalchemy_uri: sqlalchemy_uri
					};
					this.$axios.post('/database/test', data).then(res => {
						console.log(res);
						if (res.data.code == 0) {
							this.$refs[form].validate(valid => {
								if (valid) {
									let { display_name, sqlalchemy_uri } = this.form;
									let data = {
										display_name: display_name,
										sqlalchemy_uri: sqlalchemy_uri
									};
									this.$axios.post('/database/add', data).then(res => {
										console.log(res);
										if (res.data.code == 0) {
											this.$message({
												message: '添加成功',
												type: 'success'
											});
											location.reload()
											this.dialogFormVisible = false;
										} else {
											this.$message({
												message: res.data.message,
												type: 'error'
											});
										}
									});
								}
							});
						} else {
							this.$message({
								message: res.data.message,
								type: 'error'
							});
						}
					});
				}
			});
		},
		deleteRow(index, rows) {
			let data = {
				display_name: rows[index]['display_name'],
				source: rows[index]['sqlalchemy_uri']
			};
			this.$axios.post('/database/remove', data).then(res => {
				console.log(res.data.code);
			});
			rows.splice(index, 1);
		},
		getdata(index, rows) {
			this.databoxshow=true;
			console.log(rows[index]);
			this.display_name=rows[index].display_name;
			this.sqlalchemy_uri=rows[index].sqlalchemy_uri;
			this.owner=rows[index].owner
			let data={sqlalchemy_uri:this.sqlalchemy_uri}
			this.$axios.post('/database/get_tables', data).then(res => {
				this.table_list=res.data.table_list;
			});
		}
	}
};
</script>
<style lang="less" scoped>
.root {
	height: 48.75rem;
	min-height: 6.25rem;
	.box {
		position: relative;
		left: 64.5px;
		top: -49.3625rem;
		width: 18.75rem;
		height: 49.3125rem;
		background-color: white;
		.right {
			position: relative;
			left: -10px;
			top: -12px;
		}
		.title {
			position: relative;
			top: 12px;
			left: -6.25rem;
		}
	}
	.databox {
		position: relative;
		top: -97.8125rem;
		left: 23.75rem;
		background-color: white;
		width: 71.25rem;
		height: 47.8125rem;
		border-radius:2%;
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
.dialog {
	/deep/ .el-dialog {
		height: 25rem;
		border-radius: 3%;
		box-shadow: 2px 2px 10px #000000;
	}
	.accbutton{
		position: relative;
		// background-color: red;
		left: 5.625rem;
		top: 20px;
		width: 25rem;
		height: 3.125rem;
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
