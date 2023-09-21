// Obstacle
// - Geometry
h = 1.0;
wx = 0.5;
wx05 = wx/2;
wz = 0.5;
wz05 = wz/2;
H = 8.0;
W = 3.0;
W05 = W/2;
Lin = 2.0;
Lout = 2.0;

// - Mesh
Lx = 0.7488671875;
Ly = 1.7488671875000001;
Ly_in = Ly;
Ly_out = Ly;
Ly_left = Ly;
Ly_right = Ly;
Ly_in_left = Ly;
Ly_in_right = Ly;
Ly_out_left = Ly;
Ly_out_right = Ly;

Lz = 0.7488671875;

Ne_wx = 8;
b_wx = 6.0;
Ne_wz = 10;
b_wz = 6.0;

Ne_xz = 10;
r_xz = 1.5;

Ne_y1 = 21;
r_y1 = 1.19603316910413;
b_y1 = 4.78413267641652;

Ne_x2_in = 4;
Ne_x2_out = 4;
Ne_y2 = 22;
r_y2 = 1;

Ne_z2 = 2;
r_z2 = 1.0;

// Inner (near-obstacle) region
// - Points
Point(1) = {-wx05, 0, -wz05};
Point(2) = {-wx05, 0, wz05};
Point(3) = {wx05, 0, wz05};
Point(4) = {wx05, 0, -wz05};

Point(21) = {-wx05, h, -wz05};
Point(22) = {-wx05, h, wz05};
Point(23) = {wx05, h, wz05};
Point(24) = {wx05, h, -wz05};

Point(5) = {-Lx-wx05, 0, -Lz-wz05};
Point(6) = {-Lx-wx05, 0, Lz+wz05};
Point(7) = {Lx+wx05, 0, Lz+wz05};
Point(8) = {Lx+wx05, 0, -Lz-wz05};

Point(55) = {-Lx-wx05, Ly, -Lz-wz05};
Point(56) = {-Lx-wx05, Ly, Lz+wz05};
Point(57) = {Lx+wx05, Ly, Lz+wz05};
Point(58) = {Lx+wx05, Ly, -Lz-wz05};


// All lines point in the postive x,y,z in this order of preference
// - Bottom Lines (x-z plane)
Line(1) = {1, 2};
Transfinite Curve{1} = Ne_wz Using Bump 1/b_wz;
Line(2) = {4, 3};
Transfinite Curve{2} = Ne_wz Using Bump 1/b_wz;
Line(3) = {1, 4};
Transfinite Curve{3} = Ne_wx Using Bump 1/b_wx;
Line(4) = {2, 3};
Transfinite Curve{4} = Ne_wx Using Bump 1/b_wx;

Line(5) = {5, 1};
Transfinite Curve{5} = Ne_xz Using Progression 1/r_xz;
Line(6) = {6, 2};
Transfinite Curve{6} = Ne_xz Using Progression 1/r_xz;
Line(7) = {3, 7};
Transfinite Curve{7} = Ne_xz Using Progression r_xz;
Line(8) = {4, 8};
Transfinite Curve{8} = Ne_xz Using Progression r_xz;

Line(9) = {5, 6};
Transfinite Curve{9} = Ne_wz Using Progression 1.0;
Line(10) = {6, 7};
Transfinite Curve{10} = Ne_wx Using Progression 1.0;
Line(11) = {8, 7};
Transfinite Curve{11} = Ne_wz Using Progression 1.0;
Line(12) = {5, 8};
Transfinite Curve{12} = Ne_wx Using Progression 1.0;

// - Top Obstacle Line (x-z plane)
Line(41) = {21, 22};
Transfinite Curve{41} = Ne_wz Using Bump 1/b_wz;
Line(42) = {24, 23};
Transfinite Curve{42} = Ne_wz Using Bump 1/b_wz;
Line(43) = {21, 24};
Transfinite Curve{43} = Ne_wx Using Bump 1/b_wx;
Line(44) = {22, 23};
Transfinite Curve{44} = Ne_wx Using Bump 1/b_wx;

// Oblique Lines
Line(45) = {55, 21};
Transfinite Curve{45} = Ne_xz Using Progression 1/r_xz;
Line(46) = {56, 22};
Transfinite Curve{46} = Ne_xz Using Progression 1/r_xz;
Line(47) = {23, 57};
Transfinite Curve{47} = Ne_xz Using Progression r_xz;
Line(48) = {24, 58};
Transfinite Curve{48} = Ne_xz Using Progression r_xz;

// - Top Lines (x-z plane)
Line(59) = {55, 56};
Transfinite Curve{59} = Ne_wz Using Progression 1.0;
Line(60) = {56, 57};
Transfinite Curve{60} = Ne_wx Using Progression 1.0;
Line(61) = {58, 57};
Transfinite Curve{61} = Ne_wz Using Progression 1.0;
Line(62) = {55, 58};
Transfinite Curve{62} = Ne_wx Using Progression 1.0;

// - Bottom Horizontal Surfaces:
//Line Loop(1) = {1, 4, -2, -3};
//Plane Surface(1) = {1};
Line Loop(2) = {9, 6, -1, -5};
Plane Surface(2) = {2};
Line Loop(3) = {-6, 10, -7, -4};
Plane Surface(3) = {3};
Line Loop(4) = {2, 7, -11, -8};
Plane Surface(4) = {4};
Line Loop(5) = {5, 3, 8, -12};
Plane Surface(5) = {5};

// - Verical Lines
Line(201) = {1, 21};
Transfinite Curve{201} = Ne_y1 Using Bump 1/b_y1;
Line(202) = {2, 22};
Transfinite Curve{202} = Ne_y1 Using Bump 1/b_y1;
Line(203) = {3, 23};
Transfinite Curve{203} = Ne_y1 Using Bump 1/b_y1;
Line(204) = {4, 24};
Transfinite Curve{204} = Ne_y1 Using Bump 1/b_y1;

Line(205) = {5, 55};
Transfinite Curve{205} = Ne_y1 Using Progression r_y1;
Line(206) = {6, 56};
Transfinite Curve{206} = Ne_y1 Using Progression r_y1;
Line(207) = {7, 57};
Transfinite Curve{207} = Ne_y1 Using Progression r_y1;
Line(208) = {8, 58};
Transfinite Curve{208} = Ne_y1 Using Progression r_y1;


// - Top Obstacle Surface (x-z plane)
Line Loop(6) = {41, 44, -42, -43};
Plane Surface(6) = {6};

// - Oblique Surfaces:
Line Loop(7) = {59, 46, -41, -45};
Plane Surface(7) = {7};
Line Loop(8) = {60, -47, -44, -46};
Plane Surface(8) = {8};
Line Loop(9) = {42, 47, -61, -48};
Plane Surface(9) = {9};
Line Loop(10) = {45, 43, 48, -62};
Plane Surface(10) = {10};

// - Top Surface:
Line Loop(11) = {59, 60, -61, -62};
Plane Surface(11) = {11};

// - Vertical Surfaces:
Line Loop(101) = {-1, 201, 41, -202};
Plane Surface(101) = {101};
Line Loop(102) = {-2, 204, 42, -203};
Plane Surface(102) = {102};
Line Loop(103) = {3, 204, -43, -201};
Plane Surface(103) = {103};
Line Loop(104) = {4, 203, -44, -202};
Plane Surface(104) = {104};

Line Loop(105) = {5, 201, -45, -205};
Plane Surface(105) = {105};
Line Loop(106) = {6, 202, -46, -206};
Plane Surface(106) = {106};
Line Loop(107) = {7, 207, -47, -203};
Plane Surface(107) = {107};
Line Loop(108) = {8, 208, -48, -204};
Plane Surface(108) = {108};

Line Loop(109) = {-9, 205, 59, -206};
Plane Surface(109) = {109};
Line Loop(110) = {10, 207, -60, -206};
Plane Surface(110) = {110};
Line Loop(111) = {-11, 208, 61, -207};
Plane Surface(111) = {111};
Line Loop(112) = {12, 208, -62, -205};
Plane Surface(112) = {112};

// - Bottom Solids
Surface Loop(2) = {2, 109, 106, 101, 105, 7};
Volume(2) = {2};
Surface Loop(3) = {3, 106, 110, 107, 104, 8};
Volume(3) = {3};
Surface Loop(4) = {4, 102, 107, 111, 108, 9};
Volume(4) = {4};
Surface Loop(5) = {5, 105, 103, 108, 112, 10};
Volume(5) = {5};

// - Top Solid
Surface Loop(6) = {6, 7, 8, 9, 10, 11};
Volume(6) = {6};

// Exterior
// - Bottom Points:
Point(9) = {-Lin, 0, -W05};
Point(10) = {-Lin, 0, -Lz-wz05};
Point(11) = {-Lin, 0, Lz+wz05};
Point(12) = {-Lin, 0, W05};

Point(20) = {-Lx-wx05, 0, -W05};
//Point(5) = {-Lx-wx05, 0, -Lz-wz05};
//Point(6) = {-Lx-wx05, 0, Lz+wz05};
Point(13) = {-Lx-wx05, 0, W05};

Point(19) = {Lx+wx05, 0, -W05};
//Point(8) = {Lx+wx05, 0, -Lz-wz05};
//Point(7) = {Lx+wx05, 0, Lz+wz05};
Point(14) = {Lx+wx05, 0, W05};

Point(18) = {Lout, 0, -W05};
Point(17) = {Lout, 0, -Lz-wz05};
Point(16) = {Lout, 0, Lz+wz05};
Point(15) = {Lout, 0, W05};

// - Middle Points:
Point(59) = {-Lin, Ly_in_left, -W05};
Point(60) = {-Lin, Ly_in, -Lz-wz05};
Point(61) = {-Lin, Ly_in, Lz+wz05};
Point(62) = {-Lin, Ly_in_right, W05};

Point(70) = {-Lx-wx05, Ly_left, -W05};
//Point(55) = {-Lx-wx05, Ly, -Lz-wz05};
//Point(56) = {-Lx-wx05, Ly, Lz+wz05};
Point(63) = {-Lx-wx05, Ly_right, W05};

Point(69) = {Lx+wx05, Ly_left, -W05};
//Point(58) = {Lx+wx05, Ly, -Lz-wz05};
//Point(57) = {Lx+wx05, Ly, Lz+wz05};
Point(64) = {Lx+wx05, Ly_right, W05};

Point(68) = {Lout, Ly_out_left, -W05};
Point(67) = {Lout, Ly_out, -Lz-wz05};
Point(66) = {Lout, Ly_out, Lz+wz05};
Point(65) = {Lout, Ly_out_right, W05};

// - Top Points:
Point(109) = {-Lin, H, -W05};
Point(110) = {-Lin, H, -Lz-wz05};
Point(111) = {-Lin, H, Lz+wz05};
Point(112) = {-Lin, H, W05};

Point(120) = {-Lx-wx05, H, -W05};
Point(105) = {-Lx-wx05, H, -Lz-wz05};
Point(106) = {-Lx-wx05, H, Lz+wz05};
Point(113) = {-Lx-wx05, H, W05};

Point(119) = {Lx+wx05, H, -W05};
Point(108) = {Lx+wx05, H, -Lz-wz05};
Point(107) = {Lx+wx05, H, Lz+wz05};
Point(114) = {Lx+wx05, H, W05};

Point(118) = {Lout, H, -W05};
Point(117) = {Lout, H, -Lz-wz05};
Point(116) = {Lout, H, Lz+wz05};
Point(115) = {Lout, H, W05};

// - Bottom z-Lines:
Line(13) = {9, 10};
Transfinite Curve{13} = Ne_z2 Using Progression r_z2;
Line(14) = {10, 11};
Transfinite Curve{14} = Ne_wz Using Progression 1;
Line(15) = {11, 12};
Transfinite Curve{15} = Ne_z2 Using Progression 1/r_z2;

Line(16) = {20, 5};
Transfinite Curve{16} = Ne_z2 Using Progression r_z2;
Line(17) = {6, 13};
Transfinite Curve{17} = Ne_z2 Using Progression 1/r_z2;

Line(18) = {19, 8};
Transfinite Curve{18} = Ne_z2 Using Progression r_z2;
Line(19) = {7, 14};
Transfinite Curve{19} = Ne_z2 Using Progression 1/r_z2;

Line(20) = {18, 17};
Transfinite Curve{20} = Ne_z2 Using Progression r_z2;
Line(21) = {17, 16};
Transfinite Curve{21} = Ne_wz Using Progression 1;
Line(22) = {16, 15};
Transfinite Curve{22} = Ne_z2 Using Progression 1/r_z2;

// - Middle z-Lines:
Line(63) = {59, 60};
Transfinite Curve{63} = Ne_z2 Using Progression r_z2;
Line(64) = {60, 61};
Transfinite Curve{64} = Ne_wz Using Progression 1;
Line(65) = {61, 62};
Transfinite Curve{65} = Ne_z2 Using Progression 1/r_z2;

Line(66) = {70, 55};
Transfinite Curve{66} = Ne_z2 Using Progression r_z2;
Line(67) = {56, 63};
Transfinite Curve{67} = Ne_z2 Using Progression 1/r_z2;

Line(68) = {69, 58};
Transfinite Curve{68} = Ne_z2 Using Progression r_z2;
Line(69) = {57, 64};
Transfinite Curve{69} = Ne_z2 Using Progression 1/r_z2;

Line(70) = {68, 67};
Transfinite Curve{70} = Ne_z2 Using Progression r_z2;
Line(71) = {67, 66};
Transfinite Curve{71} = Ne_wz Using Progression 1;
Line(72) = {66, 65};
Transfinite Curve{72} = Ne_z2 Using Progression 1/r_z2;

// - Top z-Lines:
Line(109) = {105, 106};
Transfinite Curve{109} = Ne_wz Using Progression 1.0;
Line(111) = {108, 107};
Transfinite Curve{111} = Ne_wz Using Progression 1;

Line(113) = {109, 110};
Transfinite Curve{113} = Ne_z2 Using Progression r_z2;
Line(114) = {110, 111};
Transfinite Curve{114} = Ne_wz Using Progression 1;
Line(115) = {111, 112};
Transfinite Curve{115} = Ne_z2 Using Progression 1/r_z2;

Line(116) = {120, 105};
Transfinite Curve{116} = Ne_z2 Using Progression r_z2;
Line(117) = {106, 113};
Transfinite Curve{117} = Ne_z2 Using Progression 1/r_z2;

Line(118) = {119, 108};
Transfinite Curve{118} = Ne_z2 Using Progression r_z2;
Line(119) = {107, 114};
Transfinite Curve{119} = Ne_z2 Using Progression 1/r_z2;

Line(120) = {118, 117};
Transfinite Curve{120} = Ne_z2 Using Progression r_z2;
Line(121) = {117, 116};
Transfinite Curve{121} = Ne_wz Using Progression 1;
Line(122) = {116, 115};
Transfinite Curve{122} = Ne_z2 Using Progression 1/r_z2;

// - Bottom x-lines:
Line(23) = {9, 20};
Transfinite Curve{23} = Ne_x2_in Using Progression 1;
Line(27) = {20, 19};
Transfinite Curve{27} = Ne_wx Using Progression 1;
Line(29) = {19, 18};
Transfinite Curve{29} = Ne_x2_out Using Progression 1;

Line(24) = {10, 5};
Transfinite Curve{24} = Ne_x2_in Using Progression 1;
Line(30) = {8, 17};
Transfinite Curve{30} = Ne_x2_out Using Progression 1;

Line(25) = {11, 6};
Transfinite Curve{25} = Ne_x2_in Using Progression 1;
Line(31) = {7, 16};
Transfinite Curve{31} = Ne_x2_out Using Progression 1;

Line(26) = {12, 13};
Transfinite Curve{26} = Ne_x2_in Using Progression 1;
Line(28) = {13, 14};
Transfinite Curve{28} = Ne_wx Using Progression 1;
Line(32) = {14, 15};
Transfinite Curve{32} = Ne_x2_out Using Progression 1;

// - Middle x-lines:
Line(73) = {59, 70};
Transfinite Curve{73} = Ne_x2_in Using Progression 1;
Line(77) = {70, 69};
Transfinite Curve{77} = Ne_wx Using Progression 1;
Line(79) = {69, 68};
Transfinite Curve{79} = Ne_x2_out Using Progression 1;

Line(74) = {60, 55};
Transfinite Curve{74} = Ne_x2_in Using Progression 1;
Line(80) = {58, 67};
Transfinite Curve{80} = Ne_x2_out Using Progression 1;

Line(75) = {61, 56};
Transfinite Curve{75} = Ne_x2_in Using Progression 1;
Line(81) = {57, 66};
Transfinite Curve{81} = Ne_x2_out Using Progression 1;

Line(76) = {62, 63};
Transfinite Curve{76} = Ne_x2_in Using Progression 1;
Line(78) = {63, 64};
Transfinite Curve{78} = Ne_wx Using Progression 1;
Line(82) = {64, 65};
Transfinite Curve{82} = Ne_x2_out Using Progression 1;

// - Top x-lines:
Line(112) = {105, 108};
Transfinite Curve{112} = Ne_wx Using Progression 1;
Line(110) = {106, 107};
Transfinite Curve{110} = Ne_wx Using Progression 1;

Line(123) = {109, 120};
Transfinite Curve{123} = Ne_x2_in Using Progression 1;
Line(127) = {120, 119};
Transfinite Curve{127} = Ne_wx Using Progression 1;
Line(129) = {119, 118};
Transfinite Curve{129} = Ne_x2_out Using Progression 1;

Line(124) = {110, 105};
Transfinite Curve{124} = Ne_x2_in Using Progression 1;
Line(130) = {108, 117};
Transfinite Curve{130} = Ne_x2_out Using Progression 1;

Line(125) = {111, 106};
Transfinite Curve{125} = Ne_x2_in Using Progression 1;
Line(131) = {107, 116};
Transfinite Curve{131} = Ne_x2_out Using Progression 1;

Line(126) = {112, 113};
Transfinite Curve{126} = Ne_x2_in Using Progression 1;
Line(128) = {113, 114};
Transfinite Curve{128} = Ne_wx Using Progression 1;
Line(132) = {114, 115};
Transfinite Curve{132} = Ne_x2_out Using Progression 1;

// - Bottom Vertical lines
Line(209) = {9, 59};
Transfinite Curve{209} = Ne_y1 Using Progression r_y1;
Line(210) = {10, 60};
Transfinite Curve{210} = Ne_y1 Using Progression r_y1;
Line(211) = {11, 61};
Transfinite Curve{211} = Ne_y1 Using Progression r_y1;
Line(212) = {12, 62};
Transfinite Curve{212} = Ne_y1 Using Progression r_y1;
Line(213) = {13, 63};
Transfinite Curve{213} = Ne_y1 Using Progression r_y1;
Line(214) = {14, 64};
Transfinite Curve{214} = Ne_y1 Using Progression r_y1;
Line(215) = {15, 65};
Transfinite Curve{215} = Ne_y1 Using Progression r_y1;
Line(216) = {16, 66};
Transfinite Curve{216} = Ne_y1 Using Progression r_y1;
Line(217) = {17, 67};
Transfinite Curve{217} = Ne_y1 Using Progression r_y1;
Line(218) = {18, 68};
Transfinite Curve{218} = Ne_y1 Using Progression r_y1;
Line(219) = {19, 69};
Transfinite Curve{219} = Ne_y1 Using Progression r_y1;
Line(220) = {20, 70};
Transfinite Curve{220} = Ne_y1 Using Progression r_y1;

// - Top Vertical lines
Line(255) = {55, 105};
Transfinite Curve{255} = Ne_y2 Using Progression 1/r_y2;
Line(256) = {56, 106};
Transfinite Curve{256} = Ne_y2 Using Progression 1/r_y2;
Line(257) = {57, 107};
Transfinite Curve{257} = Ne_y2 Using Progression 1/r_y2;
Line(258) = {58, 108};
Transfinite Curve{258} = Ne_y2 Using Progression 1/r_y2;

Line(259) = {59, 109};
Transfinite Curve{259} = Ne_y2 Using Progression 1/r_y2;
Line(260) = {60, 110};
Transfinite Curve{260} = Ne_y2 Using Progression 1/r_y2;
Line(261) = {61, 111};
Transfinite Curve{261} = Ne_y2 Using Progression 1/r_y2;
Line(262) = {62, 112};
Transfinite Curve{262} = Ne_y2 Using Progression 1/r_y2;
Line(263) = {63, 113};
Transfinite Curve{263} = Ne_y2 Using Progression 1/r_y2;
Line(264) = {64, 114};
Transfinite Curve{264} = Ne_y2 Using Progression 1/r_y2;
Line(265) = {65, 115};
Transfinite Curve{265} = Ne_y2 Using Progression 1/r_y2;
Line(266) = {66, 116};
Transfinite Curve{266} = Ne_y2 Using Progression 1/r_y2;
Line(267) = {67, 117};
Transfinite Curve{267} = Ne_y2 Using Progression 1/r_y2;
Line(268) = {68, 118};
Transfinite Curve{268} = Ne_y2 Using Progression 1/r_y2;
Line(269) = {69, 119};
Transfinite Curve{269} = Ne_y2 Using Progression 1/r_y2;
Line(270) = {70, 120};
Transfinite Curve{270} = Ne_y2 Using Progression 1/r_y2;

// - Bottom xz-plane
Line Loop(12) = {13, 24, -16, -23};
Plane Surface(12) = {12};
Line Loop(13) = {14, 25, -9, -24};
Plane Surface(13) = {13};
Line Loop(14) = {15, 26, -17, -25};
Plane Surface(14) = {14};
Line Loop(15) = {17, 28, -19, -10};
Plane Surface(15) = {15};
Line Loop(16) = {19, 32, -22, -31};
Plane Surface(16) = {16};
Line Loop(17) = {11, 31, -21, -30};
Plane Surface(17) = {17};
Line Loop(18) = {18, 30, -20, -29};
Plane Surface(18) = {18};
Line Loop(19) = {16, 12, -18, -27};
Plane Surface(19) = {19};

// - Middle xz-plane
Line Loop(22) = {63, 74, -66, -73};
Plane Surface(22) = {22};
Line Loop(23) = {64, 75, -59, -74};
Plane Surface(23) = {23};
Line Loop(24) = {65, 76, -67, -75};
Plane Surface(24) = {24};
Line Loop(25) = {67, 78, -69, -60};
Plane Surface(25) = {25};
Line Loop(26) = {69, 82, -72, -81};
Plane Surface(26) = {26};
Line Loop(27) = {61, 81, -71, -80};
Plane Surface(27) = {27};
Line Loop(28) = {68, 80, -70, -79};
Plane Surface(28) = {28};
Line Loop(29) = {66, 62, -68, -77};
Plane Surface(29) = {29};

// - Bottom xz-plane
Line Loop(31) = {109, 110, -111, -112};
Plane Surface(31) = {31};
Line Loop(32) = {113, 124, -116, -123};
Plane Surface(32) = {32};
Line Loop(33) = {114, 125, -109, -124};
Plane Surface(33) = {33};
Line Loop(34) = {115, 126, -117, -125};
Plane Surface(34) = {34};
Line Loop(35) = {117, 128, -119, -110};
Plane Surface(35) = {35};
Line Loop(36) = {119, 132, -122, -131};
Plane Surface(36) = {36};
Line Loop(37) = {111, 131, -121, -130};
Plane Surface(37) = {37};
Line Loop(38) = {118, 130, -120, -129};
Plane Surface(38) = {38};
Line Loop(39) = {116, 112, -118, -127};
Plane Surface(39) = {39};

// - Bottom Vertical Surfaces:
Line Loop(113) = {-13, 209, 63, -210};
Plane Surface(113) = {113};
Line Loop(114) = {-14, 210, 64, -211};
Plane Surface(114) = {114};
Line Loop(115) = {-15, 211, 65, -212};
Plane Surface(115) = {115};
Line Loop(116) = {-16, 220, 66, -205};
Plane Surface(116) = {116};
Line Loop(117) = {-17, 206, 67, -213};
Plane Surface(117) = {117};
Line Loop(118) = {-18, 219, 68, -208};
Plane Surface(118) = {118};
Line Loop(119) = {-19, 207, 69, -214};
Plane Surface(119) = {119};
Line Loop(120) = {-20, 218, 70, -217};
Plane Surface(120) = {120};
Line Loop(121) = {-21, 217, 71, -216};
Plane Surface(121) = {121};
Line Loop(122) = {-22, 216, 72, -215};
Plane Surface(122) = {122};

Line Loop(123) = {23, 220, -73, -209};
Plane Surface(123) = {123};
Line Loop(124) = {24, 205, -74, -210};
Plane Surface(124) = {124};
Line Loop(125) = {25, 206, -75, -211};
Plane Surface(125) = {125};
Line Loop(126) = {26, 213, -76, -212};
Plane Surface(126) = {126};
Line Loop(127) = {27, 219, -77, -220};
Plane Surface(127) = {127};
Line Loop(128) = {28, 214, -78, -213};
Plane Surface(128) = {128};
Line Loop(129) = {29, 218, -79, -219};
Plane Surface(129) = {129};
Line Loop(130) = {30, 217, -80, -208};
Plane Surface(130) = {130};
Line Loop(131) = {31, 216, -81, -207};
Plane Surface(131) = {131};
Line Loop(132) = {32, 215, -82, -214};
Plane Surface(132) = {132};

// - Top Vertical Surfaces:
Line Loop(159) = {-59, 255, 109, -256};
Plane Surface(159) = {159};
Line Loop(160) = {60, 257, -110, -256};
Plane Surface(160) = {160};
Line Loop(161) = {-61, 258, 111, -257};
Plane Surface(161) = {161};
Line Loop(162) = {62, 258, -112, -255};
Plane Surface(162) = {162};

Line Loop(163) = {-63, 259, 113, -260};
Plane Surface(163) = {163};
Line Loop(164) = {-64, 260, 114, -261};
Plane Surface(164) = {164};
Line Loop(165) = {-65, 261, 115, -262};
Plane Surface(165) = {165};
Line Loop(166) = {-66, 270, 116, -255};
Plane Surface(166) = {166};
Line Loop(167) = {-67, 256, 117, -263};
Plane Surface(167) = {167};
Line Loop(168) = {-68, 269, 118, -258};
Plane Surface(168) = {168};
Line Loop(169) = {-69, 257, 119, -264};
Plane Surface(169) = {169};
Line Loop(170) = {-70, 268, 120, -267};
Plane Surface(170) = {170};
Line Loop(171) = {-71, 267, 121, -266};
Plane Surface(171) = {171};
Line Loop(172) = {-72, 266, 122, -265};
Plane Surface(172) = {172};

Line Loop(173) = {73, 270, -123, -259};
Plane Surface(173) = {173};
Line Loop(174) = {74, 255, -124, -260};
Plane Surface(174) = {174};
Line Loop(175) = {75, 256, -125, -261};
Plane Surface(175) = {175};
Line Loop(176) = {76, 263, -126, -262};
Plane Surface(176) = {176};
Line Loop(177) = {77, 269, -127, -270};
Plane Surface(177) = {177};
Line Loop(178) = {78, 264, -128, -263};
Plane Surface(178) = {178};
Line Loop(179) = {79, 268, -129, -269};
Plane Surface(179) = {179};
Line Loop(180) = {80, 267, -130, -258};
Plane Surface(180) = {180};
Line Loop(181) = {81, 266, -131, -257};
Plane Surface(181) = {181};
Line Loop(182) = {82, 265, -132, -264};
Plane Surface(182) = {182};

// - Solids
// - - Bottom:
Surface Loop(12) = {12, 113, 124, 116, 123, 22};
Volume(12) = {12};
Surface Loop(13) = {13, 114, 125, 109, 124, 23};
Volume(13) = {13};
Surface Loop(14) = {14, 115, 126, 117, 125, 24};
Volume(14) = {14};
Surface Loop(15) = {15, 117, 128, 119, 110, 25};
Volume(15) = {15};
Surface Loop(16) = {16, 119, 132, 122, 131, 26};
Volume(16) = {16};
Surface Loop(17) = {17, 111, 131, 121, 130, 27};
Volume(17) = {17};
Surface Loop(18) = {18, 118, 130, 120, 129, 28};
Volume(18) = {18};
Surface Loop(19) = {19, 116, 112, 118, 127, 29};
Volume(19) = {19};

// -- Top:
Surface Loop(11) = {11, 159, 160, 161, 162, 31};
Volume(11) = {11};
Surface Loop(22) = {22, 163, 174, 166, 173, 32};
Volume(22) = {22};
Surface Loop(23) = {23, 164, 175, 159, 174, 33};
Volume(23) = {23};
Surface Loop(24) = {24, 165, 176, 167, 175, 34};
Volume(24) = {24};
Surface Loop(25) = {25, 167, 178, 169, 160, 35};
Volume(25) = {25};
Surface Loop(26) = {26, 169, 182, 172, 181, 36};
Volume(26) = {26};
Surface Loop(27) = {27, 161, 181, 171, 180, 37};
Volume(27) = {27};
Surface Loop(28) = {28, 168, 180, 170, 179, 38};
Volume(28) = {28};
Surface Loop(29) = {29, 166, 162, 168, 177, 39};
Volume(29) = {29};

Transfinite Surface "*";
Recombine Surface "*";
Transfinite Volume "*";
Recombine Volume "*";

Mesh 3;
SetOrder 2;

// Boundaries:
// Wall
// - Bottom: 2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19
// - Top: 31, 32, 33, 34, 35, 36, 37, 38, 39
// - Left: 123, 127, 129, 173, 177, 179
// - Right: 126, 128, 132, 176, 178, 182
// - Obstacle: 101, 102, 103, 104, 6
// Inlet: 113, 114, 115, 163, 164, 165
// Outlet: 120, 121, 122, 170, 171, 172


Physical Surface("inlet", 1) = {113, 114, 115, 163, 164, 165};
Physical Surface("outlet", 2) = {120, 121, 122, 170, 171, 172};
Physical Surface("bottom", 3) = {2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19};
Physical Surface("top", 4) = {31, 32, 33, 34, 35, 36, 37, 38, 39};
Physical Surface("left", 5) = {123, 127, 129, 173, 177, 179};
Physical Surface("right", 6) = {126, 128, 132, 176, 178, 182};
Physical Surface("obstacle", 7) = {101, 102, 103, 104, 6};
Physical Volume("fluid", 8) = {2,3,4,5,6,12,13,14,15,16,17,18,19,11,22,23,24,25,26,27,28,29};
