<template>
	<div>
		<router-view />
	</div>
</template>
<script>
export default {
	components: {},
	setup() {}
};
</script>
<style lang="less">
#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
}
body {
	background-color: #f5f5f5;
	height: 100%;
	margin: 0;
	width: 100%;
	overflow-x: hidden;
}
html {
	height: 100%;
	width: 100%;
	overflow-y: scroll;
}
:root {
	overflow-y: auto;
	overflow-x: hidden;
}
:root body {
	position: absolute;
}

.heightAll {
	height: 100%;
}
.mainNavigation {
	position: fixed;
	height: 100%;
	width: 100%;
}
.el-menu-vertical-demo:not(.el-menu--collapse) {
	height: 100%;
}
#nav {
	padding: 30px;
	a {
		font-weight: bold;
		color: #2c3e50;

		&.router-link-exact-active {
			color: #42b983;
		}
	}
}
</style>
